from rest_framework import serializers

from biller.config import Configurations
from biller_apps.common.dataclasses.search import Search


class SearchSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=100, required=False,default='')
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)

    def create(self, validated_data) -> Search:
        return Search(**validated_data)
