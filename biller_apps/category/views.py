import json

import pandas
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.category.dataclasses.request.delete import CategoryDeleteRequest
from biller_apps.category.dataclasses.request.delete_many import CategoryDeleteManyRequest
from biller_apps.category.dataclasses.request.update import CategoryUpdateRequest
from biller_apps.category.es_query import CategoryEsQuery
from biller_apps.category.models import Category
from biller_apps.category.serializers.request.create import CategoryRequest
from biller_apps.category.utils import CategoryUtils
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.organisation.models import Organisation


class CategoryView:
    def __init__(self):
        self.data_created = "Category added successfully"
        self.data_created_error_exist = "Category name already exists"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Category delete successfully"
        self.data_no_match = "No matching category found"
        self.data_update = "Category updated successfully"

        super().__init__()

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: CategoryRequest, token_payload: Payload):
        with transaction.atomic():
            organisation_id = Organisation.get(company_name=token_payload.organisationName, single=True)['organisation_id']
            Category().create(name=params.name, organisation_name=token_payload.organisationName,
                              organisation_id=organisation_id)
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(Category.get(organisation_name=token_payload.organisationName, params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        items = pages.page(params.page_num)
        data = json.loads(CategoryUtils().mapper(items.object_list))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url,
                                        total_page=pages.num_pages, total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: CategoryDeleteRequest, token_payload: Payload):
        category = Category().get_with_code(category_code=params.category_code,
                                            organisation_name=token_payload.organisationName)
        if category is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Category().remove(category_id=category['category_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: CategoryUpdateRequest, token_payload: Payload):
        category = Category().get_with_code(category_code=params.category_code,
                                            organisation_name=token_payload.organisationName)
        if category is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Category().update(category_id=category['category_id'], name=params.name)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: CategoryDeleteManyRequest, token_payload: Payload):
        brand = Category().get_with_code_list(category_code=params.category_code,
                                              organisation_name=token_payload.organisationName)
        if len(brand) != len(params.category_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(brand)
        category_ids = dataframe['category_id'].tolist()
        with transaction.atomic():
            Category().remove_from_list(category_ids=category_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = CategoryEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
