from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer


class StatusGetAllSerializer(serializers.Serializer):
    statusId = serializers.CharField()
    status = serializers.CharField()
    progress = serializers.IntegerField()


class StatusDataSerializer(APiResponseSerializer):
    data = StatusGetAllSerializer()
