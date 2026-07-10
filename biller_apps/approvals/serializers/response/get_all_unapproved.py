from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class ApproverDataSerializer(serializers.Serializer):
    requestFrom = serializers.CharField()
    requestMethod = serializers.CharField()
    payload = serializers.CharField()
    approvalCode = serializers.CharField()


class ApproverGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=ApproverDataSerializer())


class ApproverDataResponseSerializer(APiResponseSerializer):
    data = ApproverGetAllSerializer()
