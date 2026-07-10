from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.organisation.dataclasses.request.delete import OrganisationDelete


class OrganisationDeleteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data) -> OrganisationDelete:
        return OrganisationDelete(**validated_data)

    @staticmethod
    def get_parameters():
        return [OpenApiParameter(name='name', description='name of the organisation',
                                 required=True, type=OpenApiTypes.STR,
                                 location=OpenApiParameter.QUERY)
                ]
