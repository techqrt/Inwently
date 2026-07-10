from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers


from biller_apps.storage.dataclasses.request.get import StorageGet


class StorageGetSerializer(serializers.Serializer):
    bucket_name = serializers.CharField(max_length=100)
    file_name = serializers.CharField(max_length=100)
    dummy = serializers.BooleanField(default=False)

    def create(self, validated_data) -> StorageGet:
        return StorageGet(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='bucket_name', description='bucket_name of the bucket',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='file_name', description='file_name of the file',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='dummy', description='return the response as json from Minio file',
                             required=False, type=OpenApiTypes.BOOL,
                             location=OpenApiParameter.QUERY),

        ]