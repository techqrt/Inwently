from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.return_purchase.dataclasses.request.get import ReturnPurchaseGet


class ReturnPurchaseGetSerializer(GetSerializer):
    return_code = serializers.CharField()

    def create(self, validated_data) -> ReturnPurchaseGet:
        return ReturnPurchaseGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='return_code', description='return_code of the Return Purchase',
                                                   required=True, type=OpenApiTypes.INT,
                                                   location=OpenApiParameter.QUERY))

        return default_parameters
