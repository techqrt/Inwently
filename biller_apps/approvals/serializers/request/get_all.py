from rest_framework import serializers

from biller.config import Configurations
from biller_apps.approvals.dataclasses.request.get_all import ApprovalsGetAllRequest


class ApprovalsGetAllSerializer(serializers.Serializer):
    values = serializers.CharField(max_length=100, default='', required=False)
    limit = serializers.IntegerField(default=Configurations.pagination_count, required=False)
    page_num = serializers.IntegerField(default=1, required=False)

    def create(self, validated_data) -> ApprovalsGetAllRequest:
        return ApprovalsGetAllRequest(**validated_data)
