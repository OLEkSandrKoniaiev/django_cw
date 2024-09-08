from django.db import models

from core.models import BaseModel


class DealershipModel(BaseModel):
    class Meta:
        db_table = 'dealerships'
        ordering = ('id',)

    name = models.CharField(max_length=255)
    # admin = models.ForeignKey(
    #     'users.UserModel',
    #     on_delete=models.CASCADE,
    #     related_name='dealerships'
    # )
    address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=13)
    website = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # logo = models.ImageField(upload_to=FileService., blank=True)
