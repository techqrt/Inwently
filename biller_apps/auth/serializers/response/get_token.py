from rest_framework import serializers


class GetTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
