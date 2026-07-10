from rest_framework import serializers

from biller_apps.taxes.dataclases.request.update import TaxesUpdate


class TaxesUpdateRequestSerializer(serializers.Serializer):
    tax_code = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    total_tax = serializers.FloatField(default=0.0)
    tax_splits = serializers.JSONField(default=dict)

    def create(self, validated_data) -> TaxesUpdate:
        return TaxesUpdate(**validated_data)
