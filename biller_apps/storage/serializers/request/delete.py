from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.storage.dataclasses.request.delete import DeleteGet


class DeleteGetSerializer(serializers.Serializer):
    bucket_name = serializers.CharField(max_length=100)
    file_name = serializers.CharField(max_length=100)

    def create(self, validated_data) -> DeleteGet:
        return DeleteGet(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(name='bucket_name', description='bucket_name of the bucket',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='file_name', description='file_name of the file',
                             required=True, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
        ]
