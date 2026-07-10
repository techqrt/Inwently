from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class BillDataSerializer(serializers.Serializer):
    billNumber = serializers.CharField()
    createdAt = serializers.DateTimeField()
    quantity = serializers.IntegerField()
    totalPrice = serializers.DecimalField(decimal_places=2, max_digits=10)
    itemName = serializers.CharField()
    billedBy = serializers.CharField()
    shopCode = serializers.CharField()


class BillGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=BillDataSerializer())


class BillDataResponseSerializer(APiResponseSerializer):
    data = BillGetAllSerializer()
