# biller_apps/customer_quotation/controller.py
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.customer_quotation.serializers.request.create import CustomerQuotationCreateSerializer
from biller_apps.customer_quotation.serializers.request.review import CustomerQuotationReviewSerializer
from biller_apps.customer_quotation.serializers.request.get import CustomerQuotationGetSerializer
from biller_apps.customer_quotation.serializers.request.get_all import CustomerQuotationGetAllSerializer
from biller_apps.customer_quotation.views import CustomerQuotationView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class CustomerQuotationViewController:

    @extend_schema(description="Submit a customer quotation", request=CustomerQuotationCreateSerializer)
    @api_view(['POST'])
    @SerializerValidations(serializer=CustomerQuotationCreateSerializer).validate
    def create(request: Request) -> Response:
        return CustomerQuotationView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(description="Review a quotation (phone confirm / reject / cancel)",
                    request=CustomerQuotationReviewSerializer)
    @api_view(['PUT'])
    @SerializerValidations(serializer=CustomerQuotationReviewSerializer).validate
    def review(request: Request) -> Response:
        return CustomerQuotationView().review_extract(params=request.params, token_payload=request.payload)

    @extend_schema(parameters=[
            OpenApiParameter(
                name="customer_quotation_id",
                description="Customer quotation ID",
                required=False,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="customer_quotation_code",
                description="Customer quotation code",
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ])
    @api_view(['GET'])
    @SerializerValidations(serializer=CustomerQuotationGetSerializer).validate
    def get(request: Request) -> Response:
        return CustomerQuotationView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(description="Get all customer quotations")
    @api_view(['GET'])
    @SerializerValidations(serializer=CustomerQuotationGetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return CustomerQuotationView().get_all_extract(params=request.params, token_payload=request.payload)