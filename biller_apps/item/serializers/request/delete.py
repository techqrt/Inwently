from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.item.dataclasses.request.delete import ItemDelete


class ItemDeleteSerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> ItemDelete:
        return ItemDelete(**validated_data)

    @staticmethod
    def get_parameters():
        return [OpenApiParameter(name='item_code', description='name of the Item',
                                 required=True, type=OpenApiTypes.STR,
                                 location=OpenApiParameter.QUERY)
                ]
