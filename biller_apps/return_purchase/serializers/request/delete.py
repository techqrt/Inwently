from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.return_purchase.dataclasses.request.delete import ReturnPurchaseDelete


class ReturnPurchaseDeleteSerializer(serializers.Serializer):
    return_code = serializers.CharField()

    def create(self, validated_data) -> ReturnPurchaseDelete:
        return ReturnPurchaseDelete(**validated_data)

    def get_parameters(self) -> list:
        return [
            OpenApiParameter(name='return_code', description='return_code of the Return Purchase',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
