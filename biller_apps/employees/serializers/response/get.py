from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from rest_framework import serializers

from biller_apps.employees.serializers.response.get_all import PermissionsSerializer

class ShopAccessSerializer(serializers.Serializer):
    name = serializers.CharField()
    shopCode = serializers.CharField()

class EmployeesGetDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    mobileNumber = serializers.CharField(required=False, allow_blank=True)
    alternatemobilenumber = serializers.CharField(required=False, allow_blank=True)
    dob = serializers.DateField(input_formats=['%Y-%m-%d'])
    state = serializers.CharField()
    country = serializers.CharField()
    street = serializers.CharField()
    organisationName = serializers.CharField()
    shopAccess = serializers.ListField(child=ShopAccessSerializer())
    isActive = serializers.BooleanField()
    emailId = serializers.EmailField()
    emailVerified = serializers.BooleanField()
    profilePhotoUrl = serializers.CharField(required=False, allow_blank=True)
    employeeCode = serializers.CharField()
    permissions = PermissionsSerializer()

class EmployeesGetResponseSerializer(APiResponseSerializer):
    data = EmployeesGetDataSerializer()
