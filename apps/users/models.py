from django.core import validators as V
from django.db import models


class PhoneNumberModel(models.Model):
    class Meta:
        db_table = 'phone_numbers'
        ordering = ('id',)

    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=12, validators=(V.MinLengthValidator(10)), blank=False, null=False)
