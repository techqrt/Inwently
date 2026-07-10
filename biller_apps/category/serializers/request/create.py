from rest_framework import serializers

from biller_apps.category.dataclasses.request.create import CategoryRequest


class CategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data) -> CategoryRequest:
        return CategoryRequest(**validated_data)
