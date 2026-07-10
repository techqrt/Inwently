from rest_framework import serializers

from biller_apps.shops.dataclases.request.delete_many import ShopsDeleteMany


class ShopDeleteManySerializer(serializers.Serializer):
    shop_code = serializers.ListField(required=True)

    def create(self, validated_data) -> ShopsDeleteMany:
        return ShopsDeleteMany(**validated_data)
