from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.shops.dataclases.request.delete import ShopsDelete


class ShopsDeleteSerializer(serializers.Serializer):
    shop_code = serializers.CharField(max_length=50)

    def create(self, validated_data) -> ShopsDelete:
        return ShopsDelete(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='shop_code', description='shop_code of the shop', required=True,
                             type=OpenApiTypes.STR, location=OpenApiParameter.QUERY)
        ]
