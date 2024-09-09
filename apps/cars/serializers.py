from django.db import transaction

from rest_framework import serializers

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
            'created_at'
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
        if not CarModel.objects.can_update_car(car=instance):
            raise serializers.ValidationError("Updates can be made no more than once a day or the car is inactive.")

        if not CarModel.objects.has_changes(car=instance, validated_data=validated_data):
            raise serializers.ValidationError("No changes have been made.")

        model = validated_data.pop('model', None)
        if model and isinstance(model, int):
            model = ModelModel.objects.get(id=model)
        if model:
            instance.model = model

        profile_data = validated_data.pop('car_profile', None)
        if profile_data:
            CarProfileModel.objects.filter(car=instance).update(**profile_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# class CarPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarModel
#         fields = ('photo',)
#         extra_kwargs = {'photo': {'required': True}}
