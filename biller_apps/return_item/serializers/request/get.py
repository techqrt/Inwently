from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.return_item.dataclasses.request.get import ReturnItemGet


class ReturnItemGetSerializer(GetSerializer):
    return_code = serializers.CharField()

    def create(self, validated_data) -> ReturnItemGet:
        return ReturnItemGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='return_code', description='return_code of the Return Item',
                                                   required=True, type=OpenApiTypes.INT,
                                                   location=OpenApiParameter.QUERY))

        return default_parameters
