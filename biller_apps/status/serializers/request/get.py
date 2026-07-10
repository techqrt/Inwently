from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.status.dataclasses.request.get import StatusGet


class StatusGetSerializer(serializers.Serializer):
    status_id = serializers.CharField(max_length=100)

    def create(self, validated_data) -> StatusGet:
        return StatusGet(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='status_id', description='status_id of the status',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
