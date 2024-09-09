from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.utils import timezone

from rest_framework import serializers

from core.services.email_service import EmailService

from apps.users.models import ProfileModel

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'city', 'phone', 'created_at', 'updated_at')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('name', 'surname', 'age', 'city', 'phone', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        now = timezone.now()

        has_changes = False
        for field, value in validated_data.items():
            if getattr(instance, field) != value:
                has_changes = True
                break

        if not has_changes:
            raise serializers.ValidationError("No changes detected.")

        if instance.updated_at and (now - instance.updated_at).days < 30:
            raise serializers.ValidationError("You can only update your profile once a month.")

        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_premium',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'profile',
            'dealership_id'
        )
        read_only_fields = (
            'id',
            'is_active',
            'is_premium',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    @atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)
        if profile_data:
            ProfileModel.objects.filter(user=user).update(**profile_data)
        return user

    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        EmailService.register_email(user)
        return user


class UserDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password.")
        return value
