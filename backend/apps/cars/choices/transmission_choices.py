from django.db import models


class TransmissionChoices(models.TextChoices):
    MANUAL = 'Manual', 'Manual'
    AUTOMATIC = 'Automatic', 'Automatic'
