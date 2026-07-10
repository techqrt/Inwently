from rest_framework import serializers

from biller_apps.billing.dataclasses.request.create import BillingRequest


class BillingRequestSerializer(serializers.Serializer):
    items = serializers.ListField(default=[{'item_code': None, 'quantity': None}])

    def create(self, validated_data) -> BillingRequest:
        return BillingRequest(**validated_data)
