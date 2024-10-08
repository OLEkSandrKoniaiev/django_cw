from datetime import datetime

from django.core import validators as V
from django.db import models

from core.models import BaseModel, PriceModel
from core.services.file_service import FileService

from apps.cars.choices.body_choices import BodyChoices
from apps.cars.choices.engine_choices import EngineChoices
from apps.cars.choices.region_choices import RegionChoices
from apps.cars.choices.transmission_choices import TransmissionChoices
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
    price = models.ForeignKey(PriceModel, on_delete=models.SET_NULL, related_name='cars', null=True)
    is_new = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    edit_attempts = models.IntegerField(default=2)
    user = models.ForeignKey(
        'users.UserModel',
        on_delete=models.CASCADE,
        null=True,
        related_name='cars'
    )
    objects = CarManager()


class CarProfileModel(BaseModel):
    class Meta:
        db_table = 'car_profiles'
        ordering = ('id',)

    city = models.CharField(max_length=60)
    region = models.CharField(max_length=16, choices=RegionChoices.choices)
    description = models.CharField(max_length=255)
    color = models.CharField(max_length=120)
    owner_number = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(100)))
    mileage = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(999_999)))
    engine = models.CharField(max_length=7, choices=EngineChoices.choices)
    engine_capacity = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(100)), null=True)
    transmission = models.CharField(max_length=9, choices=TransmissionChoices.choices)
    body = models.CharField(max_length=9, choices=BodyChoices.choices)
    car = models.OneToOneField(CarModel, on_delete=models.CASCADE, related_name='car_profile')
    photo = models.ImageField(upload_to=FileService.upload_car_photo, blank=True, null=True)


class ViewModel(models.Model):
    class Meta:
        db_table = 'views'
        ordering = ('id',)

    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='views')
    created_at = models.DateTimeField(auto_now_add=True)
