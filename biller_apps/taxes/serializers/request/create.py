from rest_framework import serializers

from biller_apps.taxes.dataclases.request.create import TaxesCreate


class TaxesGetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    total_tax = serializers.FloatField(default=0.0)
    tax_splits = serializers.JSONField(default=dict)

    def create(self, validated_data) -> TaxesCreate:
        return TaxesCreate(**validated_data)
