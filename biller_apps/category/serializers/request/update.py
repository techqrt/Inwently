from rest_framework import serializers

from biller_apps.category.dataclasses.request.update import CategoryUpdateRequest


class CategoryUpdateRequestSerializer(serializers.Serializer):
    category_code = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data) -> CategoryUpdateRequest:
        return CategoryUpdateRequest(**validated_data)
