from django.db.transaction import atomic

from rest_framework import serializers

from apps.dealerships.models import DealershipModel


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipModel
        fields = ('id', 'name', 'admin_id', 'address', 'contact_phone', 'website', 'description')
        read_only_fields = ('admin_id',)

    @atomic
    def create(self, validated_data):
        user = self.context['request'].user
        return DealershipModel.objects.create(admin_id=user, **validated_data)
