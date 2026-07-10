from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class ShopGetAllDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    isActive = serializers.BooleanField()
    organisationName = serializers.CharField()
    createdDateTime = serializers.DateTimeField()
    state = serializers.CharField()
    street = serializers.CharField()
    country = serializers.CharField()
    isActiveChangeTime = serializers.DateTimeField()
    shopCode = serializers.CharField()
    website = serializers.CharField(allow_blank=True)
    emailId = serializers.EmailField()
    mobileNumber = serializers.CharField()
    altMobileNumber = serializers.CharField(allow_blank=True)
    type = serializers.CharField()


class ShopGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=ShopGetAllDataSerializer())


class ShopDataSerializer(APiResponseSerializer):
    data = ShopGetAllSerializer()
