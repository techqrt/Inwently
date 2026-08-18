from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.pos.serializers.request.create import POSCreateSerializer
from biller_apps.pos.serializers.request.update import POSUpdateSerializer
from biller_apps.pos.serializers.request.status_change import POSStatusChangeSerializer
from biller_apps.pos.serializers.request.get import POSGetSerializer
from biller_apps.pos.serializers.request.get_all import POSGetAllSerializer
from biller_apps.pos.serializers.request.delete import POSDeleteSerializer
from biller_apps.pos.views import POSView


class POSViewController:

    @extend_schema(
        description="Create a POS draft with items",
        request=POSCreateSerializer,
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=POSCreateSerializer).validate
    def create(request: Request) -> Response:
        return POSView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a POS draft (add/update/remove items, header fields) — draft status only",
        request=POSUpdateSerializer,
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=POSUpdateSerializer).validate
    def update(request: Request) -> Response:
        return POSView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Mark a POS draft as sent to the customer",
        request=POSStatusChangeSerializer,
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=POSStatusChangeSerializer).validate
    def send(request: Request) -> Response:
        return POSView().send_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Mark a POS as confirmed by the customer",
        request=POSStatusChangeSerializer,
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=POSStatusChangeSerializer).validate
    def confirm(request: Request) -> Response:
        return POSView().confirm_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Cancel a POS draft",
        request=POSStatusChangeSerializer,
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=POSStatusChangeSerializer).validate
    def cancel(request: Request) -> Response:
        return POSView().cancel_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Execute a confirmed POS into the final invoice (checks and deducts inventory)",
        request=POSStatusChangeSerializer,
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=POSStatusChangeSerializer).validate
    def execute(request: Request) -> Response:
        return POSView().execute_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a single POS draft with its items",
        parameters=POSGetSerializer.get_parameters(),
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=POSGetSerializer).validate
    def get(request: Request) -> Response:
        return POSView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
    description="Get all POS records",
    parameters=POSGetAllSerializer.get_all_parameters(),
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=POSGetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return POSView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a POS draft (only if not yet executed)",
        request=POSDeleteSerializer,
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=POSDeleteSerializer).validate
    def delete(request: Request) -> Response:
        return POSView().delete_extract(params=request.params, token_payload=request.payload)