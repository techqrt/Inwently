from rest_framework import serializers

from biller_apps.auth.dataclasses.request.forgot_password import ForgotPassword


class ForgotPasswordRequestSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    email_otp = serializers.IntegerField()
    new_password = serializers.CharField(max_length=30)


    def create(self, validated_data) -> ForgotPassword:
        return ForgotPassword(**validated_data)
