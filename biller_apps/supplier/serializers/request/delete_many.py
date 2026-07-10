from rest_framework import serializers

from biller_apps.supplier.dataclasses.request.delete_many import SupplierDeleteManyRequest


class SupplierDeleteManySerializer(serializers.Serializer):
    supplier_code = serializers.ListField(required=True)

    def create(self, validated_data) -> SupplierDeleteManyRequest:
        return SupplierDeleteManyRequest(**validated_data)
