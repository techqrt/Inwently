from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.auth.dataclasses.request.auth_activate import RegisterRequest


class RegisterRequestSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    email_otp = serializers.IntegerField()
    password = serializers.CharField(max_length=30)

    def create(self, validated_data) -> RegisterRequest:
        return RegisterRequest(**validated_data)


