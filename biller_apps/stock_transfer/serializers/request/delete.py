from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.stock_transfer.dataclasses.request.delete import StockTransferDelete


class StockTransferDeleteSerializer(serializers.Serializer):
    transfer_code = serializers.CharField(max_length=50)

    def create(self, validated_data) -> StockTransferDelete:
        return StockTransferDelete(**validated_data)

    def get_parameters(self) -> list:
        return [
            OpenApiParameter(name='transfer_code', description='transfer_code of the stock transfer',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
