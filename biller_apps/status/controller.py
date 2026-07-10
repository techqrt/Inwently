from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage
from biller_apps.status.serializers.request.get import StatusGetSerializer
from biller_apps.status.serializers.response.get import StatusDataSerializer
from biller_apps.status.views import StatusView


class StatusController:
    @extend_schema(
        description="Get the status of a task",
        parameters=StatusGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=StatusDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=StatusGetSerializer).validate
    def get(request: Request) -> Response:
        return StatusView().get_extract(params=request.params)
