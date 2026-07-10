from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.purchase.dataclasses.request.get import PurchaseGet


class PurchaseGetSerializer(GetSerializer):
    purchase_code = serializers.CharField()

    def create(self, validated_data) -> PurchaseGet:
        return PurchaseGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='purchase_code', description='purchase_code of the Purchase',
                                                   required=True, type=OpenApiTypes.INT,
                                                   location=OpenApiParameter.QUERY))

        return default_parameters
