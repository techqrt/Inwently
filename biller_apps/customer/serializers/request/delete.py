from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.customer.dataclasses.request.delete import CustomerDelete


class CustomerDeleteSerializer(serializers.Serializer):
    customer_code = serializers.CharField(max_length=50)

    def create(self, validated_data) -> CustomerDelete:
        return CustomerDelete(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='customer_code', description='customer_code is the unique id of a customer',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY)
        ]
