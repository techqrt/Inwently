from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.inventory.dataclasses.request.get import InventoryGet


class InventoryGetSerializer(serializers.Serializer):
    inventory_id = serializers.IntegerField(required=False, default=None, allow_null=True)
    inventory_code = serializers.CharField(max_length=25, required=False, default=None, allow_null=True,
                                            allow_blank=True)

    def create(self, validated_data) -> InventoryGet:
        return InventoryGet(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name='inventory_id',
                description='Lookup by inventory_id (either this or inventory_code is required)',
                required=False,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='inventory_code',
                description='Lookup by inventory_code, e.g. "T_5-T_2" (either this or inventory_id is required)',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            ),
        ]