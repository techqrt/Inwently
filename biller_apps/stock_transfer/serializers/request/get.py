from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.stock_transfer.dataclasses.request.get import StockTransferGet


class StockTransferGetSerializer(GetSerializer):
    transfer_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> StockTransferGet:
        return StockTransferGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='transfer_code', description='transfer_code of the stock transfer',
                                                   required=True, type=OpenApiTypes.INT,
                                                   location=OpenApiParameter.QUERY))

        return default_parameters
