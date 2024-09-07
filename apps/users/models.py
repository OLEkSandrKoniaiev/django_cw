from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.models import BaseModel

# from apps.dealerships.models import DealershipModel
from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ('id',)

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    is_premium = models.BooleanField(default=False)
    dealership_id = models.ForeignKey(
        'dealerships.DealershipModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )


class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ('id',)

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.IntegerField()
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
