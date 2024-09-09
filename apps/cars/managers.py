from django.db import models
from django.utils import timezone

from rest_framework.exceptions import ValidationError


class CarManager(models.Manager):
    def create_car(self, user, **kwargs):
        if not user.is_premium and self.filter(user=user).count() >= 1:
            raise ValidationError("Non-premium users can only add one car.")
        return self.create(user=user, **kwargs)

    @staticmethod
    def can_update_car(car):
        if car.is_active:
            now = timezone.now()
            if (now - car.updated_at).total_seconds() > 86400:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def has_changes(car, validated_data):
        for field, value in validated_data.items():
            if getattr(car, field) != value:
                return True
        return False
