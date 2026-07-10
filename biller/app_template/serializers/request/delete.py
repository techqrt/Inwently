from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.app_template.dataclasses.request.delete import AppTemplateDeleteRequest


class AppTemplateDeleteRequestSerializer(serializers.Serializer):


    def create(self, validated_data) -> AppTemplateDeleteRequest:
        return AppTemplateDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            
        ]
