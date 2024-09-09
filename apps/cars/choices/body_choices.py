from django.db import models


class BodyTypeChoices(models.TextChoices):
    HATCHBACK = 'HatchBack', 'HatchBack'
    SEDAN = 'Sedan', 'Sedan'
    COUPE = 'Coupe', 'Coupe'
    WAGON = 'Wagon', 'Wagon'
    JEEP = 'Jeep', 'Jeep'
