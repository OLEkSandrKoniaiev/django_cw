from django.db import transaction

from rest_framework import serializers

from core.services.email_service import EmailService

from apps.cars.models import BrandModel, CarModel, CarProfileModel, ModelModel


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = ('id', 'name')


class ModelSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=BrandModel.objects.all())

    class Meta:
        model = ModelModel
        fields = ('id', 'name', 'brand')

    def create(self, validated_data):
        brand = validated_data.pop('brand')
        if isinstance(brand, int):
            brand = BrandModel.objects.get(id=brand)
        validated_data['brand'] = brand
        return super().create(validated_data)


class CarProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarProfileModel
        fields = (
            'id',
            'city',
            'region',
            'description',
            'color',
            'owner_number',
            'mileage',
            'engine',
            'engine_capacity',
            'transmission',
            'body',
            'updated_at',
            'created_at',
            'photo'
        )


class CarSerializer(serializers.ModelSerializer):
    car_profile = CarProfileSerializer()
    model = serializers.PrimaryKeyRelatedField(queryset=ModelModel.objects.all())

    class Meta:
        model = CarModel
        fields = (
            'id',
            'model',
            'year',
            'price',
            'currency',
            'is_new',
            'is_active',
            'edit_attempts',
            'user',
            'created_at',
            'updated_at',
            'car_profile'
        )
        read_only_fields = (
            'id',
            'is_active',
            'created_at',
            'updated_at'
        )

    @transaction.atomic
    def create(self, validated_data):
        model = validated_data.pop('model')
        if isinstance(model, int):
            model = ModelModel.objects.get(id=model)
        validated_data['model'] = model

        profile_data = validated_data.pop('car_profile')
        request = self.context.get('request', None)
        validated_data['user'] = request.user
        car = CarModel.objects.create_car(**validated_data)
        CarProfileModel.objects.create(car=car, **profile_data)
        return car

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.is_active:
            if not CarModel.objects.can_update_car(car=instance):
                raise serializers.ValidationError("Updates can be made no more than once a day.")
        if not CarModel.objects.has_changes(car=instance, validated_data=validated_data):
            raise serializers.ValidationError("No changes have been made.")

        if instance.edit_attempts >= 0:
            if not CarModel.objects.bad_words_check(car=instance, validated_data=validated_data):
                instance.edit_attempts -= 1
                instance.is_active = False
                instance.save()
                return instance, "You have bad words, please try again."
            instance.is_active = True
            instance.edit_attempts = 2
        else:
            EmailService.check_badwords_email(user_id=instance.user_id, car_id=instance.id)
            raise serializers.ValidationError("No more attempts left.")

        profile_data = validated_data.pop('car_profile', None)
        if profile_data:
            car_profile = instance.car_profile
            for field, value in profile_data.items():
                setattr(car_profile, field, value)
            car_profile.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
