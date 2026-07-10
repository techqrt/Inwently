from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.organisation.dataclasses.request.get import OrganisationGet


class OrganisationGetSerializer(GetSerializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data) -> OrganisationGet:
        return OrganisationGet(**validated_data)

    @staticmethod
    def get_parameters(default_parameters: list = SwaggerPage.get_parameters()):
        default_parameters.append(OpenApiParameter(name='name', description='name of the organisation',
                                                   required=True, type=OpenApiTypes.STR,
                                                   location=OpenApiParameter.QUERY))
        return default_parameters
