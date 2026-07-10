from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class CategoryDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    categoryCode = serializers.CharField()


class CategoryGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=CategoryDataSerializer())


class CategoryGetAllResponseSerializer(APiResponseSerializer):
    data = CategoryGetAllSerializer()
