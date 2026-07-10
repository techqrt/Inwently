from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage
from biller_apps.places.serializers.request.get import PlacesGetSerializer
from biller_apps.places.views import PlaceView


# noinspection PyMethodParameters
class PlaceViewController:

    @extend_schema(
        description="Get all country or states",
        parameters=PlacesGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description="[]")
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=PlacesGetSerializer).validate
    def get(request: Request) -> Response:
        return PlaceView().get_extract(params=request.params)
