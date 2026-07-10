from rest_framework import serializers

from biller_apps.item.dataclasses.request.delete_many import ItemDeleteManyRequest


class ItemDeleteManySerializer(serializers.Serializer):
    item_code = serializers.ListField(required=True)

    def create(self, validated_data) -> ItemDeleteManyRequest:
        return ItemDeleteManyRequest(**validated_data)
