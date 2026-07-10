from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage
from biller_apps.pos.serializers.request.create import POSSerializer
from biller_apps.pos.views import POSView


class POSViewController:

    @extend_schema(
        description="Create a POS transaction",
        request=POSSerializer,
        responses=SwaggerPage.response(description=POSView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=POSSerializer,
                           exec_func='POSView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return POSView().create_extract(params=request.params, token_payload=request.payload)
