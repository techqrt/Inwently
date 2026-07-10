from rest_framework import serializers

from biller_apps.auth.dataclasses.request.password_change import PasswordChange


class PasswordChangeRequestSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def create(self, validated_data) -> PasswordChange:
        return PasswordChange(**validated_data)
