from django.db import models

from core.models import BaseModel


class DealershipModel(BaseModel):
    class Meta:
        db_table = 'dealerships'
        ordering = ('id',)

    name = models.CharField(max_length=255)
    admin_id = models.ForeignKey('users.UserModel', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_phone = models.CharField(max_length=12, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    # logo = models.ImageField(upload_to=FileService., blank=True)
