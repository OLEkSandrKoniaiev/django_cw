from decimal import Decimal

import requests
from celery import shared_task
from celery.beat import Service

from core.exceptions.currency_exception import CurrencyException
from core.models import CurrencyModel, PriceModel

PRIVATBANK_API_URL = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'


class CurrencyService(Service):
    @staticmethod
    @shared_task
    def update_currency(*args, **kwargs):
        response = requests.get(PRIVATBANK_API_URL)

        if response.status_code == 200:
            data = response.json()
            for item in data:
                name = item['ccy']
                if name in ['USD', 'EUR']:
                    buy_price = Decimal(item['buy'])
                    sale_price = Decimal(item['sale'])

                    CurrencyModel.objects.update_or_create(
                        name=name,
                        defaults={
                            'buy': buy_price,
                            'sell': sale_price
                        }
                    )
            CurrencyService.update_car_prices.delay()
        else:
            raise CurrencyException

    @staticmethod
    @shared_task
    def update_car_prices():
        usd_rate_sell = CurrencyModel.objects.get(name='USD').sell
        usd_rate_buy = CurrencyModel.objects.get(name='USD').buy
        eur_rate_sell = CurrencyModel.objects.get(name='EUR').sell
        eur_rate_buy = CurrencyModel.objects.get(name='EUR').buy

        for car_price in PriceModel.objects.all():
            if car_price.initial_currency == 'USD':
                car_price.price_in_USD = car_price.initial_price
                car_price.price_in_EUR = car_price.initial_price * usd_rate_buy / eur_rate_sell
                car_price.price_in_UAH = car_price.initial_price * usd_rate_buy
            elif car_price.initial_currency == 'EUR':
                car_price.price_in_EUR = car_price.initial_price
                car_price.price_in_USD = car_price.initial_price * eur_rate_buy / usd_rate_sell
                car_price.price_in_UAH = car_price.initial_price * eur_rate_buy
            elif car_price.initial_currency == 'UAH':
                car_price.price_in_UAH = car_price.initial_price
                car_price.price_in_USD = car_price.initial_price / usd_rate_sell
                car_price.price_in_EUR = car_price.initial_price / eur_rate_sell
            car_price.save()
