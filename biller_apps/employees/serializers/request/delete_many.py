from rest_framework import serializers

from biller_apps.employees.dataclasses.request.delete_many import EmployeeDeleteManyRequest


class EmployeeDeleteManySerializer(serializers.Serializer):
    employee_code = serializers.ListField(required=True)

    def create(self, validated_data) -> EmployeeDeleteManyRequest:
        return EmployeeDeleteManyRequest(**validated_data)
