from django.core import validators as V
from django.db import models

from core.enums.regex_enum import RegexEnum
from core.models import BaseModel


class DealershipModel(BaseModel):
    class Meta:
        db_table = 'dealerships'
        ordering = ('id',)

    name = models.CharField(max_length=255)
    admin = models.ForeignKey(
        'users.UserModel',
        on_delete=models.CASCADE,
        null=True,
        related_name='dealerships'
    )
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, validators=[V.RegexValidator(*RegexEnum.PHONE.value)])
    website = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # logo = models.ImageField(upload_to=FileService., blank=True)
