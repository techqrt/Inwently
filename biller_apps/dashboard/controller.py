from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.swagger import SwaggerPage
from biller_apps.dashboard.views import DashboardView


# noinspection PyMethodParameters
class DashboardController:
    @extend_schema(
        description="Get the count of organisation,shops,employees and devices for web dashboard",
        responses=SwaggerPage.response(description=DashboardView().data_fetched)
    )
    @api_view(['GET'])
    def web_count(request: Request) -> Response:
        return DashboardView().web_count(request)
