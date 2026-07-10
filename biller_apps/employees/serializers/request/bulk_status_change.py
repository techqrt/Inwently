from rest_framework import serializers

from biller_apps.employees.dataclasses.request.bulk_status_change import EmployeeBulkStatusChangeRequest



class EmployeeBulkStatusChangeSerializer(serializers.Serializer):
    employee_code = serializers.ListField(required=True)
    status = serializers.BooleanField(required=True)

    def create(self, validated_data) -> EmployeeBulkStatusChangeRequest:
        return EmployeeBulkStatusChangeRequest(**validated_data)