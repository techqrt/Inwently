from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.approvals.dataclasses.request.status_change import ApprovalsStatusChangeRequest


class ApprovalsStatusChangeSerializer(serializers.Serializer):
    approval_code = serializers.CharField(max_length=10)
    approved = serializers.BooleanField()

    def create(self, validated_data) -> ApprovalsStatusChangeRequest:
        return ApprovalsStatusChangeRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='approval_code', description='approval_code of the approval',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='approved', description='approved of the approval',
                             required=True, type=OpenApiTypes.BOOL,
                             location=OpenApiParameter.QUERY)
        ]
