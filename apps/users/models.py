from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators as V
from django.db import models

from core.models import BaseModel

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ('id',)

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    dealership_id = models.IntegerField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ('id',)

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(validators=[V.MinValueValidator(18), V.MaxValueValidator(90)])
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
