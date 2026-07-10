from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.item.dataclasses.request.get import ItemGet


class ItemGetSerializer(GetSerializer):
    item_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> ItemGet:
        return ItemGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='item_code', description='supplier_code of the supplier',
                                                   required=True, type=OpenApiTypes.STR,
                                                   location=OpenApiParameter.QUERY))

        return default_parameters
