from rest_framework import serializers

from biller_apps.auth.dataclasses.response.login_extract import LoginResponse


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.EmailField()
    refresh_token = serializers.CharField()

    def create(self, validated_data) -> LoginResponse:
        return LoginResponse(**validated_data)
