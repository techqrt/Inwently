from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class SuppliersDataSerializer(serializers.Serializer):
    organisationName = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    street = serializers.CharField()
    name = serializers.CharField()
    isActive = serializers.BooleanField()
    mobileNumber = serializers.CharField()
    emailId = serializers.EmailField()
    createdDateTime = serializers.DateTimeField()
    altMobileNumber = serializers.CharField()
    supplierCode = serializers.CharField()
    idNumber = serializers.CharField()
    idType = serializers.CharField()
    gstNumber = serializers.CharField()
    photoUrl = serializers.URLField()
    idProofUrl = serializers.URLField()


class SupplierGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=SuppliersDataSerializer())


class SupplierDataSerializer(APiResponseSerializer):
    data = SupplierGetAllSerializer()
