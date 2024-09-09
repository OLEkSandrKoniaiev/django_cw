from django.db import models

from rest_framework.exceptions import ValidationError


class CarManager(models.Manager):
    def create_car(self, user, **kwargs):
        if not user.is_premium and self.filter(user=user).count() >= 1:
            raise ValidationError("Non-premium users can only add one car.")
        return self.create(user=user, **kwargs)
