from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class CustomerDataSerializer(serializers.Serializer):
    organisationName = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    street = serializers.CharField()
    name = serializers.CharField()
    isActive = serializers.BooleanField()
    mobileNumber = serializers.CharField()
    emailId = serializers.EmailField()
    createdDateTime = serializers.DateTimeField()
    customerCode = serializers.CharField()
    idNumber = serializers.CharField()
    idType = serializers.CharField()
    occupation = serializers.CharField()
    photoUrl = serializers.URLField()
    idProofUrl = serializers.URLField()
    dateOfBirth = serializers.DateField()
    gender = serializers.CharField()
    martial_status = serializers.CharField()
    religion = serializers.CharField()
    bloodGroup = serializers.CharField()
    education = serializers.CharField()


class CustomerGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=CustomerDataSerializer())


class CustomerGetAllResponseSerializer(APiResponseSerializer):
    data = CustomerGetAllSerializer()
