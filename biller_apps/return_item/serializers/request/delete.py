from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.return_item.dataclasses.request.delete import ReturnItemDelete


class ReturnItemDeleteSerializer(serializers.Serializer):
    return_code = serializers.CharField()

    def create(self, validated_data) -> ReturnItemDelete:
        return ReturnItemDelete(**validated_data)

    def get_parameters(self) -> list:
        return [
            OpenApiParameter(name='return_code', description='return_code of the Return Item',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
