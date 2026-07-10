from rest_framework import serializers

from biller_apps.category.dataclasses.request.delete_many import CategoryDeleteManyRequest


class CategoryDeleteManySerializer(serializers.Serializer):
    category_code = serializers.ListField(required=True)

    def create(self, validated_data) -> CategoryDeleteManyRequest:
        return CategoryDeleteManyRequest(**validated_data)
