from rest_framework import serializers

from biller_apps.app_template.dataclasses.request.create import AppTemplateRequest


class AppTemplateRequestSerializer(serializers.Serializer):


    def create(self, validated_data) -> AppTemplateRequest:
        return AppTemplateRequest(**validated_data)
