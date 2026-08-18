# biller_apps/pos/serializers/request/get.py
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.pos.dataclasses.request.get import POSGet


class POSGetSerializer(serializers.Serializer):
    pos_id = serializers.IntegerField(required=False)
    pos_code = serializers.CharField(required=False)

    def create(self, validated_data) -> POSGet:
        return POSGet(**validated_data)

    @classmethod
    def get_parameters(cls):
        return [
            OpenApiParameter(
                name="pos_id",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="POS id — either this or pos_code is required.",
            ),
            OpenApiParameter(
                name="pos_code",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="POS code — either this or pos_id is required.",
            ),
        ]