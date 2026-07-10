from rest_framework import serializers

from biller_apps.employees.dataclasses.request.update import EmployeesUpdateRequest
from biller_apps.employees.serializers.request.create import PermissionsRequestSerializer



class EmployeesUpdateRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    mobile_number = serializers.CharField(max_length=20)
    alternate_mobile_number = serializers.CharField(max_length=20)
    dob = serializers.DateField()
    shop_access = serializers.ListField()
    email_id = serializers.EmailField()
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    profile_photo_url = serializers.CharField(default=None, allow_blank=True, allow_null=True,required=False)
    permissions = PermissionsRequestSerializer()
    employee_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> EmployeesUpdateRequest:
        return EmployeesUpdateRequest(**validated_data)
