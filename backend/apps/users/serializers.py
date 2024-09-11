from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from core.services.email_service import EmailService

from apps.users.models import ProfileModel

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'city', 'phone', 'created_at', 'updated_at')


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
            'updated_at',
            'dealership_id'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        if not UserModel.objects.can_update_user(user=instance):
            raise serializers.ValidationError("Updates can be made no more than once every 5 minutes.")

        if not UserModel.objects.has_changes(user=instance, validated_data=validated_data):
            raise serializers.ValidationError("No changes have been made.")

        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)
        if profile_data:
            ProfileModel.objects.filter(user=user).update(**profile_data)
        return user

    @transaction.atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        EmailService.register_email(user)
        return user
