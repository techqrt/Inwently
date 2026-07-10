from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class OrganisationDataSerializer(serializers.Serializer):
    ownerName = serializers.CharField()
    ownerMobile = serializers.CharField()
    createdDateTime = serializers.DateTimeField()
    state = serializers.CharField()
    street = serializers.CharField()
    country = serializers.CharField()
    approval = serializers.BooleanField()
    plan = serializers.CharField(max_length=100)
    planExpiry = serializers.DateField()


class OrganisationGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=OrganisationDataSerializer())



class OrganisationGetAllResponseSerializer(APiResponseSerializer):
    data = OrganisationGetAllSerializer()
