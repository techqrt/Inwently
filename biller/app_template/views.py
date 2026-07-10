import json


from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload

from biller_apps.brand.dataclasses.request.delete_many import BrandDeleteManyRequest

from biller_apps.brand.utils import BrandUtils
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils



class AppTemplateView:
    def __init__(self):
        self.data_created = "app_template added successfully"
        self.data_created_error_exist = "app_template already exists"
        self.data_get = "Data fetched successfully"
        self.data_delete = "app_template delete successfully"
        self.data_no_match = "No matching brand found"
        self.data_update = "app_template updated successfully"

        super().__init__()

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, token_payload):
        # add the business logic here
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        # add the business logic here
        pages = Paginator([], params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        data = json.loads(BrandUtils().mapper(data.object_list))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, token_payload: Payload):
        # add the business logic here
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, token_payload: Payload):
        # add the business logic here
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: BrandDeleteManyRequest, token_payload: Payload):
        # add the business logic here
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data, total_pages, total_count = AppTemplateEsQuery().search_pattern_start_with_query(request_keys=params.key,
                                                                                        organisation_id=token_payload.organisation_id,
                                                                                        limit=params.limit,
                                                                                        page_num=params.page_num)
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=total_pages,
                                        total_count=total_count,
                                        next_page_required=True if total_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
