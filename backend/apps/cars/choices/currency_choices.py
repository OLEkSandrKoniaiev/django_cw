from django.db import models


class CurrencyChoices(models.TextChoices):
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    UAH = 'UAH', 'UAH'
