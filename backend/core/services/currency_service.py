from celery import shared_task


class CurrencyService:
    @staticmethod
    @shared_task
    def update_currency(*args, **kwargs):
        pass
