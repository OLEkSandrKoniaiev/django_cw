from django.db import transaction

from rest_framework import serializers

from apps.dealerships.models import DealershipModel


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipModel
        fields = (
            'id',
            'name',
            'address',
            'phone',
            'website',
            'description',
            'created_at',
            'updated_at',
            'user'
        )
        read_only_fields = ('created_at', 'updated_at', 'user')

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request', None)
        validated_data['user'] = request.user
        dealership = DealershipModel.objects.create(**validated_data)
        return dealership
