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
        now = timezone.now()
        if (now - car.updated_at).total_seconds() > 86400:
            return True
        else:
            return False

    @staticmethod
    def has_changes(car, validated_data):
        for field, value in validated_data.items():
            if getattr(car, field) != value:
                return True
        return False

    @staticmethod
    def bad_words_check(car, validated_data):
        bad_words = ('fuck',)

        car_data = car.__dict__.copy()

        for field, value in validated_data.items():
            if field != 'car_profile':
                car_data[field] = value

        for field, value in car_data.items():
            if isinstance(value, str):
                if any(bad_word in value.lower() for bad_word in bad_words):
                    return False

        car_profile_data = car.car_profile.__dict__.copy()

        if 'car_profile' in validated_data:
            profile_data = validated_data['car_profile']
            for field, value in profile_data.items():
                car_profile_data[field] = value

        for field, value in car_profile_data.items():
            if isinstance(value, str):
                if any(bad_word in value.lower() for bad_word in bad_words):
                    return False

        return True


