from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage
from biller_apps.inventory.serializers.request.create import InventoryCreateSerializer
from biller_apps.inventory.serializers.request.get import InventoryGetSerializer
from biller_apps.inventory.serializers.request.get_all import InventoryGetAllSerializer
from biller_apps.inventory.serializers.request.update import InventoryUpdateSerializer
from biller_apps.inventory.serializers.response.get_all import InventoryDataSerializer
from biller_apps.inventory.views import InventoryView


class InventoryViewController:

    @extend_schema(
        description="Create an Inventory item",
        request=InventoryCreateSerializer,
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=InventoryCreateSerializer).validate
    def create(request: Request) -> Response:
        return InventoryView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a single Inventory item",
        parameters=InventoryGetSerializer.get_parameters(),
        responses=InventoryDataSerializer,
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=InventoryGetSerializer).validate
    def get(request: Request) -> Response:
        return InventoryView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update an Inventory item",
        request=InventoryUpdateSerializer,
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=InventoryUpdateSerializer).validate
    def update(request: Request) -> Response:
        return InventoryView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Inventory items",
        parameters=InventoryGetAllSerializer.get_all_parameters(),
        responses=SwaggerPage.response(response=InventoryDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=InventoryGetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return InventoryView().get_all_extract(params=request.params, token_payload=request.payload)