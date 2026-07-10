from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.billing.dataclasses.request.delete import BillingDeleteRequest


class BillingDeleteSerializer(serializers.Serializer):
    bill_number = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data) -> BillingDeleteRequest:
        return BillingDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='bill_number', description='bill_number to be deleted',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY)

        ]
