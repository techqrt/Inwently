from rest_framework import serializers

from biller_apps.storage.dataclasses.request.upload import UploadGet


class UploadGetSerializer(serializers.Serializer):
    bucket_name = serializers.CharField(max_length=100)
    file_name = serializers.CharField(max_length=100)
    files = serializers.CharField(default="base64 encoded string")

    def create(self, validated_data) -> UploadGet:
        return UploadGet(**validated_data)
