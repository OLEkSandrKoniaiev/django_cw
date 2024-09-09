from django.db import models


class BodyChoices(models.TextChoices):
    HATCHBACK = 'HatchBack', 'HatchBack'
    SEDAN = 'Sedan', 'Sedan'
    COUPE = 'Coupe', 'Coupe'
    WAGON = 'Wagon', 'Wagon'
    JEEP = 'Jeep', 'Jeep'
