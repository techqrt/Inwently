import json

import pandas
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.brand.dataclasses.request.delete import BrandDeleteRequest
from biller_apps.brand.dataclasses.request.delete_many import BrandDeleteManyRequest
from biller_apps.brand.dataclasses.request.update import BrandUpdateRequest
from biller_apps.brand.es_query import BrandEsQuery
from biller_apps.brand.models import Brand
from biller_apps.brand.serializers.request.create import BrandRequest
from biller_apps.brand.utils import BrandUtils
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.organisation.models import Organisation


class BrandView:
    def __init__(self):
        self.data_created = "Brand added successfully"
        self.data_created_error_exist = "Brand name already exists"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Brand delete successfully"
        self.data_no_match = "No matching brand found"
        self.data_update = "Brand updated successfully"

        super().__init__()

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: BrandRequest, token_payload):
        with transaction.atomic():
            organisation = Organisation.get(company_name=token_payload.organisationName, single=True)
            Brand.brand_check_name_exist(name=params.name, organisation_name=token_payload.organisationName)
            Brand().create(name=params.name, organisation_name=token_payload.organisationName,
                           organisation_id=organisation['organisation_id'])
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(Brand.get(organisation_name=token_payload.organisationName,params=params), params.limit)
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
    def delete_extract(self, params: BrandDeleteRequest, token_payload: Payload):
        brand = Brand().get_with_code(brand_code=params.brand_code, organisation_name=token_payload.organisationName)
        if brand is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Brand().remove(brand_id=brand['brand_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: BrandUpdateRequest, token_payload: Payload):
        brand = Brand().get_with_code(brand_code=params.brand_code, organisation_name=token_payload.organisationName)
        if brand is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Brand().update(brand_id=brand['brand_id'], name=params.name)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: BrandDeleteManyRequest, token_payload: Payload):
        brand = Brand().get_with_code_list(brand_code=params.brand_code,
                                           organisation_name=token_payload.organisationName)
        if len(brand) != len(params.brand_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(brand)
        brand_ids = dataframe['brand_id'].tolist()
        with transaction.atomic():
            Brand.remove_from_list(brand_ids=brand_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        print("params.key",params.key,"token_payload.organisation_id",token_payload.organisation_id)
        data=BrandEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        print("data",data)
        return Response(status=status.HTTP_200_OK,data=Utils.success_response_data(message=self.data_get,data=data))