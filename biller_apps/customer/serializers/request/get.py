from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers


from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.customer.dataclasses.request.get import CustomerGet


class CustomerGetSerializer(GetSerializer):
    customer_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> CustomerGet:
        return CustomerGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='customer_code', description='customer_code of the customer',
                                                   required=True, type=OpenApiTypes.STR,
                                                   location=OpenApiParameter.QUERY))

        return default_parameters
