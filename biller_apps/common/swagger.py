from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from rest_framework import status

from biller.config import Configurations
from biller.constants import Constants
from biller_apps.common.utils import Utils


class SwaggerPage:

    @staticmethod
    def get_all_parameters():
        return [
            OpenApiParameter(name='value', description='column required with coma separated',
                             required=False, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='page_num', description='page number to get the list of records',
                             required=False, type=OpenApiTypes.INT,
                             location=OpenApiParameter.QUERY),
            OpenApiParameter(name='limit', description='number of data in a single page', required=False,
                             type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                             default=Configurations.pagination_count),
            OpenApiParameter(name='sort_by', description='Field to sort by', required=False,
                             type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, default='name'),
            OpenApiParameter(name='sort_order', description='Sort by Ascending or Descending',
                             required=False,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['asc', 'desc']),
            OpenApiParameter(name='filter_key', description='Field to filter by (e.g., "is_active")',
                             required=False,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['is_active']
            ),
            OpenApiParameter(name='filter_value', description='Value for the filter field (e.g., "true" or "false" for "is_active")',
                             required=False,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['true','false']),
            OpenApiParameter(name='search_key', description='Field to search by (e.g., "name")',required=False,location=OpenApiParameter.QUERY,type=str)

        ]

    @staticmethod
    def search_parameters(key_description: str):
        return [
            OpenApiParameter(name='key', description=key_description,
                             required=False, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY)
        ]

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='value', description='column required with coma separated',
                             required=False, type=OpenApiTypes.STR,
                             location=OpenApiParameter.QUERY)
        ]

    @staticmethod
    def response(description: str = None, response=None, auth=False):
        resp = {status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description=str(Utils.error_response_data(message="", error=[])))}
        if auth:
            resp[status.HTTP_401_UNAUTHORIZED] = OpenApiResponse(
                description=str(Utils.error_response_data(message=Constants.auth_error, error=[])))

        if description is not None:
            resp[status.HTTP_200_OK] = OpenApiResponse(
                description=str(Utils.success_response_data(message=description)))
        elif response is not None:
            resp[status.HTTP_200_OK] = OpenApiResponse(response=response)
        return resp

    @staticmethod
    def get_generate_excel_pdf_parameters():
        """Parameters for downloading reports in Excel or PDF format."""
        return [
            OpenApiParameter(name='module_type', description='Type of module (e.g., "overview_report")',
                             required=True, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='download_type', description='Download format (pdf/excel)',
                             required=True, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                             enum=['pdf', 'excel']),
            OpenApiParameter(name='filter_key', description='Field to filter data',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='filter_value', description='Value for the filter field',
                             required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='title', description='Title of the report',
                             required=True, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY)
        ]