from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.inventory.serializers.request.get_all import InventoryGetAllSerializer
from biller_apps.inventory.serializers.response.get_all import InventoryDataSerializer
from biller_apps.inventory.views import InventoryView


class InventoryViewController:

    @extend_schema(
        description="Get all Inventory items",
        parameters=InventoryGetAllSerializer.get_all_parameters(),
        responses=SwaggerPage.response(response=InventoryDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=InventoryGetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return InventoryView().get_all_extract(params=request.params, token_payload=request.payload)