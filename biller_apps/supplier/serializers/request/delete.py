from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.supplier.dataclasses.request.delete import SupplierDelete


class SupplierDeleteSerializer(serializers.Serializer):
    supplier_code = serializers.CharField(max_length=50)

    def create(self, validated_data) -> SupplierDelete:
        return SupplierDelete(**validated_data)

    def get_parameters(self) -> list:
        return [
            OpenApiParameter(name='supplier_code', description='supplier_code of the supplier',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
