from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.shops.dataclases.request.get import ShopGet


class ShopGetSerializer(GetSerializer):
    shop_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> ShopGet:
        return ShopGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='shop_code', description='shop_code of the shop', required=True,
                                                   type=OpenApiTypes.STR, location=OpenApiParameter.QUERY))

        return default_parameters
