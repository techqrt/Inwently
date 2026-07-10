from rest_framework import serializers

from biller_apps.app_template.dataclasses.request.update import AppTemplateUpdateRequest


class AppTemplateUpdateRequestSerializer(serializers.Serializer):


    def create(self, validated_data) -> AppTemplateUpdateRequest:
        return AppTemplateUpdateRequest(**validated_data)
