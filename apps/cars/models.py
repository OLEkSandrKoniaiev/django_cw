from datetime import datetime

from django.core import validators as V
from django.db import models

from core.models import BaseModel
from core.services.file_service import FileService

from apps.auth.views import UserModel
from apps.auto_parks.models import AutoParkModel
from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.choices.currency_choices import CurrencyChoices
from apps.cars.managers import CarManager


class BrandModel(BaseModel):
    class Meta:
        db_table = 'brands'
        ordering = ('id',)

    name = models.CharField(unique=True, max_length=120)


class ModelModel(BaseModel):
    class Meta:
        db_table = 'models'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='unique_model_brand')
        ]

    name = models.CharField(max_length=120)
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, related_name='models')


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ('-id',)

    model = models.ForeignKey(ModelModel, on_delete=models.CASCADE, related_name='cars')
    year = models.IntegerField(validators=(V.MinValueValidator(1900), V.MaxValueValidator(datetime.now().year)))
    price = models.IntegerField(validators=(V.MinValueValidator(100), V.MaxValueValidator(100_000_000)))
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices)
    is_new = models.BooleanField(default=False)
    # user = models.ForeignKey(
    #     'users.UserModel',
    #     on_delete=models.CASCADE,
    #     related_name='cars'
    # )
    # brand = models.CharField(max_length=10, validators=(V.MinLengthValidator(2),))
    # body_type = models.CharField(max_length=9, choices=BodyTypeChoices.choices, blank=False, null=False)
    # auto_park = models.ForeignKey(AutoParkModel, on_delete=models.CASCADE, related_name='cars')
    # photo = models.ImageField(upload_to=FileService.upload_car_photo, blank=True)

    objects = CarManager()


# class CarProfileView(BaseModel):
#     class Meta:
#         db_table = 'car_profiles'
#         ordering = ('id',)
#
#     city =
#     car = models.OneToOneField(CarModel, on_delete=models.CASCADE, related_name='car_profiles')
