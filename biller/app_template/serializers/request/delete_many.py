from rest_framework import serializers

from biller_apps.app_template.dataclasses.request.delete_many import AppTemplateDeleteManyRequest


class AppTemplateDeleteManySerializer(serializers.Serializer):


    def create(self, validated_data) -> AppTemplateDeleteManyRequest:
        return AppTemplateDeleteManyRequest(**validated_data)
