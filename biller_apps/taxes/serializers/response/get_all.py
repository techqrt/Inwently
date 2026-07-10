from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class TaxSplitsSerializer(serializers.Serializer):
    cgst = serializers.FloatField()
    sgst = serializers.FloatField()


class TaxDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    totalTax = serializers.FloatField()
    taxSplits = TaxSplitsSerializer()
    taxCode = serializers.CharField()


class TaxesGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=TaxDataSerializer())


class TaxesGetAllResponseSerializer(APiResponseSerializer):
    data = TaxesGetAllSerializer()
