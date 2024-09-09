from rest_framework import serializers

from apps.cars.models import BrandModel, CarModel, CarProfileModel, ModelModel


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = ('name',)


class ModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = ModelModel
        fields = ('name', 'brand')


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
    model = ModelSerializer()

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

# class CarPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarModel
#         fields = ('photo',)
#         extra_kwargs = {'photo': {'required': True}}
