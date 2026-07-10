from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.employees.dataclasses.request.get import EmployeeGet


class EmployeeGetSerializer(GetSerializer):
    employee_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> EmployeeGet:
        return EmployeeGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()) -> list:
        default_parameters.append(OpenApiParameter(name='employee_code', description='employee_code of the employee',
                                                   required=True, type=OpenApiTypes.STR,
                                                   location=OpenApiParameter.QUERY))
        return default_parameters
