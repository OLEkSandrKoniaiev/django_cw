from rest_framework import serializers

from apps.dealerships.models import DealershipModel


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipModel
        fields = ('id', 'name', 'admin_id', 'address', 'contact_phone', 'website', 'description')
