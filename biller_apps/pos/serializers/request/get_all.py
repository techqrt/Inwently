# biller_apps/pos/serializers/request/get_all.py — add to the existing class
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.pos.dataclasses.request.get_all import POSGetAll


class POSGetAllSerializer(serializers.Serializer):
    page_num = serializers.IntegerField(min_value=1, default=1)
    limit = serializers.IntegerField(min_value=1, max_value=100, default=20)
    status = serializers.ChoiceField(
        choices=[
            "draft", "sent_to_customer", "confirmed",
            "inventory_pending", "inventory_confirmed",
            "dispatch_pending", "dispatch_confirmed",
            "ready_for_execution", "cancelled", "executed",
        ],
        required=False,
    )
    sort_by = serializers.ChoiceField(choices=["created_date", "amount"], default="created_date")
    sort_order = serializers.ChoiceField(choices=["asc", "desc"], default="desc")

    def create(self, validated_data) -> POSGetAll:
        return POSGetAll(**validated_data)

    @classmethod
    def get_all_parameters(cls):
        return [
            OpenApiParameter(name="page_num", type=int, location=OpenApiParameter.QUERY, required=False, description="Page number, default 1."),
            OpenApiParameter(name="limit", type=int, location=OpenApiParameter.QUERY, required=False, description="Page size, default 20, max 100."),
            OpenApiParameter(name="status", type=str, location=OpenApiParameter.QUERY, required=False,
                              description="Filter by status: draft, sent_to_customer, confirmed, cancelled, executed."),
            OpenApiParameter(name="sort_by", type=str, location=OpenApiParameter.QUERY, required=False, description="created_date or amount."),
            OpenApiParameter(name="sort_order", type=str, location=OpenApiParameter.QUERY, required=False, description="asc or desc."),
        ]