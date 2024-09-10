from django.db import models


class EngineChoices(models.TextChoices):
    PETROL = 'Petrol', 'Petrol'
    DIESEL = 'Diesel', 'Diesel'
    ELECTRO = 'Electro', 'Electro'
