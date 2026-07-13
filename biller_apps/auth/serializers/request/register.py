from rest_framework import serializers

from biller_apps.auth.dataclasses.request.auth_activate import RegisterRequest
from biller_apps.employees.serializers.request.create import PermissionsRequestSerializer


class RegisterRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    mobile_number = serializers.CharField(max_length=20)
    alternate_mobile_number = serializers.CharField(max_length=20, required=False, default=None, allow_null=True, allow_blank=True)
    dob = serializers.DateField()
    shop_access = serializers.ListField()
    email_id = serializers.EmailField()
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    profile_photo_url = serializers.CharField(default=None, allow_blank=True, allow_null=True)
    permissions = PermissionsRequestSerializer()
    organisation_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=30)

    def create(self, validated_data) -> RegisterRequest:
        return RegisterRequest(**validated_data)
