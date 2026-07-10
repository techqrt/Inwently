from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.shops.dataclases.request.get_all import ShopGetAll


class ShopGetAllSerializer(GetAllSerializer):
    type = serializers.CharField(max_length=100, required=False, default=None)

    def create(self, validated_data) -> ShopGetAll:
        return ShopGetAll(**validated_data)

    @staticmethod
    def get_parameters():
        parent_parameters = SwaggerPage.get_all_parameters()
        parent_parameters.append(OpenApiParameter(name='type', description='type of shop either branch or warehouse',
                                                  required=False, type=OpenApiTypes.STR,
                                                  location=OpenApiParameter.QUERY))
        return parent_parameters
