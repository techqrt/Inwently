from rest_framework import serializers

from biller_apps.taxes.dataclases.request.delete_many import TaxesDeleteMany


class TaxesDeleteManyRequestSerializer(serializers.Serializer):
    tax_codes = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data) -> TaxesDeleteMany:
        return TaxesDeleteMany(**validated_data)
