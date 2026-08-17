# biller_apps/customer_quotation/serializers/request/get_all.py
from rest_framework import serializers
from biller_apps.customer_quotation.dataclasses.request.get_all import CustomerQuotationGetAll


class CustomerQuotationGetAllSerializer(serializers.Serializer):
    page_num = serializers.IntegerField(min_value=1, default=1)
    limit = serializers.IntegerField(min_value=1, max_value=100, default=20)
    status = serializers.ChoiceField(
        choices=["pending", "phone_confirmed", "rejected", "cancelled", "converted"],
        required=False,
    )
    sort_by = serializers.ChoiceField(choices=["created_at", "status"], default="created_at")
    sort_order = serializers.ChoiceField(choices=["asc", "desc"], default="desc")

    def create(self, validated_data) -> CustomerQuotationGetAll:
        return CustomerQuotationGetAll(**validated_data)