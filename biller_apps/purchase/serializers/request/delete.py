from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.purchase.dataclasses.request.delete import PurchaseDelete


class PurchaseDeleteSerializer(serializers.Serializer):
    purchase_code = serializers.CharField()

    def create(self, validated_data) -> PurchaseDelete:
        return PurchaseDelete(**validated_data)

    def get_parameters(self) -> list:
        return [
            OpenApiParameter(name='purchase_code', description='purchase_code of the Purchase',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
