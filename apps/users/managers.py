from django.contrib.auth.models import UserManager as Manager
from django.utils import timezone


class UserManager(Manager):

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields['is_active'] is not True:
            raise ValueError('Superuser must have is_active=True')
        if extra_fields['is_staff'] is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields['is_superuser'] is not True:
            raise ValueError('Superuser must have is_superuser=True')
        user = self.create_user(email, password, **extra_fields)
        return user

    @staticmethod
    def has_changes(user, validated_data):
        for field, value in validated_data.items():
            if getattr(user, field) != value:
                return True
        return False

    @staticmethod
    def can_update_user(user):
        now = timezone.now()
        if (now - user.updated_at).total_seconds() > 86400 * 30:
            return True
        else:
            return False
