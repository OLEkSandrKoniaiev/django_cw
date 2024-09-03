from datetime import datetime

from django.core import validators as V
from django.db import models

from core.models import BaseModel

from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.choices.status_choices import StatusChoices


class BrandModel(models.Model):
    class Meta:
        db_table = 'brands'
        ordering = ('id',)

    name = models.CharField(max_length=50, blank=False, null=False)


class ModelModel(models.Model):
    class Meta:
        db_table = 'models'
        ordering = ('id',)

    brand_id = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ('id',)

    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(BrandModel, on_delete=models.CASCADE, blank=False, null=False)
    model_id = models.ForeignKey(ModelModel, on_delete=models.CASCADE, blank=False, null=False)
    price = models.IntegerField(validators=(V.MinValueValidator(100)), blank=False,
                                null=False)
    currency = models.CharField(max_length=3, blank=False, null=False)
    status = models.CharField(max_length=16, choices=StatusChoices.choices, blank=False, null=False)
    description = models.CharField(max_length=512, blank=False, null=False)
    mileage = models.IntegerField(validators=(V.MinValueValidator(0)), blank=False, null=False)
    year = models.IntegerField(validators=(V.MinValueValidator(1900), V.MaxValueValidator(datetime.now().year)))
    location = models.CharField(max_length=50, blank=False, null=False)
    car_type = models
    drive_type = models
    engine_type = models
    engine_capacity = models.IntegerField(validators=(V.MinValueValidator(0), V.MaxValueValidator(100)), blank=False,
                                          null=True)
    transmission = models
    body = models.CharField(max_length=9, choices=BodyTypeChoices.choices, blank=False, null=False)
    is_new = models.BooleanField(default=False, blank=False, null=False)


class ImageModel(models.Model):
    class Meta:
        db_table = 'images'
        ordering = ('id',)

    car_id = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to=FileService.upload_car_photo, blank=True)
