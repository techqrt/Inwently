from rest_framework import serializers

from biller_apps.storage.dataclasses.request.create import CreateGet


class CreateGetSerializer(serializers.Serializer):
    bucket_name = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data) -> CreateGet:
        return CreateGet(**validated_data)
