from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.app_template.dataclasses.request.get import AppTemplateListRequest


class AppTemplateListRequestSerializer(serializers.Serializer):


    def create(self, validated_data) -> AppTemplateListRequest:
        return AppTemplateListRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
        ]
