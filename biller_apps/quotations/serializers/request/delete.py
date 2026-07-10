from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.quotations.dataclasses.request.delete import QuotationDelete


class QuotationDeleteSerializer(serializers.Serializer):
    quotation_code = serializers.CharField()

    def create(self, validated_data) -> QuotationDelete:
        return QuotationDelete(**validated_data)

    def get_parameters(self) -> list:
        return [
            OpenApiParameter(
                name='quotation_code',
                description='Quotation code of the Quotation',
                required=True,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ]
