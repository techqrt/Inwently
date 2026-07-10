from rest_framework import serializers

from biller_apps.auth.dataclasses.request.auth_login import LoginRequest


class LoginRequestSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    def create(self, validated_data) -> LoginRequest:
        return LoginRequest(**validated_data)
