import json

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.taxes.dataclases.request.create import TaxesCreate
from biller_apps.taxes.dataclases.request.delete_many import TaxesDeleteMany
from biller_apps.taxes.dataclases.request.update import TaxesUpdate
from biller_apps.taxes.es_query import TaxesEsQuery
from biller_apps.taxes.models import Taxes
from biller_apps.taxes.utils import TaxesUtils


class TaxesView:
    def __init__(self):
        self.data_created = "Taxes added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Taxes delete successfully"
        self.data_update = "Taxes updated successfully"
        self.data_no_match = "No matching taxes found"
        self.tax_split_not_correct = "Tax split is not adding up to total tax"
        super().__init__()

    def tax_split_check(self, tax_splits: dict, total_tax_param: float):
        if len(tax_splits) > 0:
            total_tax = sum(tax_splits.values())
            if total_tax != total_tax_param:
                raise ValueError(self.tax_split_not_correct)

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: TaxesCreate, token_payload: Payload):
        self.tax_split_check(tax_splits=params.tax_splits, total_tax_param=params.total_tax)
        with transaction.atomic():
            taxes = Taxes().create(name=params.name, total_tax=params.total_tax, tax_splits=params.tax_splits,
                                   organisation_id=token_payload.organisation_id,
                                   organisation_name=token_payload.organisationName)

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        taxes = Taxes.get_all(organisation_name=token_payload.organisationName,params=params)

        pages = Paginator(taxes, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        employees_utils = TaxesUtils(columns_required=params.values_list)
        data = json.loads(employees_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    def update_extract(self, params: TaxesUpdate, token_payload: Payload):
        self.tax_split_check(tax_splits=params.tax_splits, total_tax_param=params.total_tax)
        tax = Taxes.get(organisation_name=token_payload.organisationName, tax_code=params.tax_code)
        if tax is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            taxes = Taxes().update(name=params.name, total_tax=params.total_tax, tax_splits=params.tax_splits,
                                   tax_id=tax['tax_id'])

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    @Publish.status_update
    def delete_many_extract(self, params: TaxesDeleteMany, token_payload: Payload):
        tax = Taxes.get_from_list(organisation_name=token_payload.organisationName, tax_codes=params.tax_codes)
        if len(tax) != len(params.tax_codes):
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Taxes.delete_many(organisation_name=token_payload.organisationName, tax_codes=params.tax_codes)
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):

        data= TaxesEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
