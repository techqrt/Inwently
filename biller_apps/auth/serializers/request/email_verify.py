from rest_framework import serializers

from biller_apps.auth.dataclasses.request.email_verify import EmailVerify
from biller_apps.auth.dataclasses.request.forgot_password import ForgotPassword


class EmailVerifyRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    employee_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> EmailVerify:
        return EmailVerify(**validated_data)
