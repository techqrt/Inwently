from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class EmployeeAdminReportDataSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    mobile_number = serializers.CharField(max_length=15)
    alternate_mobile_number = serializers.CharField(max_length=15, allow_blank=True, allow_null=True)
    dob = serializers.DateField()
    employee_code = serializers.CharField(max_length=100)
    email_verified = serializers.BooleanField()
    created_date_time = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    is_active_change_time = serializers.DateTimeField(allow_null=True)
    profile_photo_url = serializers.CharField(max_length=350, allow_blank=True, allow_null=True)
    street = serializers.CharField(source='address_id__street', max_length=255, allow_blank=True, allow_null=True)
    state = serializers.CharField(source='address_id__state', max_length=255, allow_blank=True, allow_null=True)
    country = serializers.CharField(source='address_id__country', max_length=255, allow_blank=True, allow_null=True)


class EmployeeAdminReportGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=EmployeeAdminReportDataSerializer())


class EmployeeAdminReportDataSerializer(APiResponseSerializer):
    data = EmployeeAdminReportGetAllSerializer()
