from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.billing.dataclasses.request.get import BillingGetRequest
from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage


class BillingGetSerializer(GetSerializer):
    bill_number = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data) -> BillingGetRequest:
        return BillingGetRequest(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(
            OpenApiParameter(name='bill_number', description='bill_number which was generated at the bill time',
                             required=True, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY)
        )

        return default_parameters
