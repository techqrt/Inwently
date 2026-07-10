from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class AppTemplateDataSerializer(serializers.Serializer):
    pass


class AppTemplateGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=AppTemplateDataSerializer())


class AppTemplateGetAllResponseSerializer(APiResponseSerializer):
    data = AppTemplateGetAllSerializer()
