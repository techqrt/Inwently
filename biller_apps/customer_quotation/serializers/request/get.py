from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.customer_quotation.dataclasses.request.get import CustomerQuotationGet


class CustomerQuotationGetSerializer(serializers.Serializer):

    customer_quotation_id = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    customer_quotation_code = serializers.CharField(
        required=False,
        allow_blank=False
    )

    def validate(self, attrs):
        quotation_id = attrs.get("customer_quotation_id")
        quotation_code = attrs.get("customer_quotation_code")

        if quotation_id is None and not quotation_code:
            raise serializers.ValidationError(
                "Either customer_quotation_id or customer_quotation_code is required."
            )

        return attrs

    def create(self, validated_data):
        return CustomerQuotationGet(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(
                name="customer_quotation_id",
                description="Customer quotation ID",
                required=False,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="customer_quotation_code",
                description="Customer quotation code",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ]