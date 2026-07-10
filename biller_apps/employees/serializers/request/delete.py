from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.employees.dataclasses.request.delete import EmployeeDelete


class EmployeeDeleteSerializer(serializers.Serializer):
    employee_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> EmployeeDelete:
        return EmployeeDelete(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='employee_code', description='employee_code of the employee',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
