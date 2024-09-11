from django.core import validators as V
from django.db import models

from apps.cars.choices.currency_choices import CurrencyChoices


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CurrencyModel(models.Model):
    class Meta:
        db_table = 'currencies'
        ordering = ('id',)

    name = models.CharField(unique=True, max_length=3)
    buy = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    sell = models.DecimalField(max_digits=8, decimal_places=2, null=True)


class PriceModel(models.Model):
    class Meta:
        db_table = 'prices'
        ordering = ('id',)

    initial_currency = models.CharField(max_length=3, choices=CurrencyChoices.choices)
    initial_price = models.DecimalField(max_digits=8, decimal_places=2,
                                        validators=(V.MinValueValidator(100), V.MaxValueValidator(100_000_000)))
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                validators=(V.MinValueValidator(100), V.MaxValueValidator(100_000_000)))
    price_in_usd = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    price_in_uan = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    price_in_eur = models.DecimalField(max_digits=8, decimal_places=2, null=True)
