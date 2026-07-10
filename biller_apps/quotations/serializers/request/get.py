from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.quotations.dataclasses.request.get import QuotationGet


class QuotationGetSerializer(GetSerializer):
    quotation_code = serializers.CharField()

    def create(self, validated_data) -> QuotationGet:
        return QuotationGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(
            OpenApiParameter(
                name='quotation_code',
                description='Quotation code of the Quotation',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            )
        )

        return default_parameters
