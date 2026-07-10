from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.places.dataclasses.request.get import PlacesGet


class PlacesGetSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=100, required=False, default=None)
    state = serializers.CharField(max_length=100, required=False, default=None)
    country_selection = serializers.BooleanField(default=True)

    def create(self, validated_data) -> PlacesGet:
        return PlacesGet(**validated_data)

    @staticmethod
    def get_parameters():
        return [OpenApiParameter(name='country', description='name of the country',
                                 required=False, type=OpenApiTypes.STR,
                                 location=OpenApiParameter.QUERY),
                OpenApiParameter(name='state', description='name of the state',
                                 required=False, type=OpenApiTypes.STR,
                                 location=OpenApiParameter.QUERY),
                OpenApiParameter(name='country_selection', description='flag to select county or state',
                                 required=False, type=OpenApiTypes.BOOL, default=True,
                                 location=OpenApiParameter.QUERY)
                ]
