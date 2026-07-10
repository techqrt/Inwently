import json

import pandas
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.exceptions.validation_errors import ValidationErrors
from biller_apps.common.models.adress import Address
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.supplier.dataclasses.request.create import SupplierRequest
from biller_apps.supplier.dataclasses.request.delete import SupplierDelete
from biller_apps.supplier.dataclasses.request.delete_many import SupplierDeleteManyRequest
from biller_apps.supplier.dataclasses.request.get import SuppliersGet
from biller_apps.supplier.dataclasses.request.update import SupplierUpdate
from biller_apps.supplier.es_query import SuppliersEsQuery
from biller_apps.supplier.models import Supplier
from biller_apps.supplier.utils import SupplierUtils


class SupplierView():
    def __init__(self):
        self.data_created = "Supplier added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Supplier delete successfully"
        self.data_update = "Supplier updated successfully"
        self.data_no_match = "No matching supplier found"
        super().__init__()

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: SupplierRequest, token_payload: Payload):

        with transaction.atomic():
            mob_unique = SupplierUtils.check_uniqueness(key='mobile_number', value=params.mobile_number,
                                                        organisation_name=token_payload.organisationName)
            email_unique = SupplierUtils.check_uniqueness(key='email_id', value=params.email_id,
                                                          organisation_name=token_payload.organisationName)
            errors = []
            if mob_unique is not None:
                errors.append(Constants.mobile_number_not_unique)
            if email_unique is not None:
                errors.append(Constants.email_id_not_unique)
            if len(errors) > 0:
                raise ValidationErrors(errors=errors)

            address_id = Address().create(state=params.state, country=params.country, street=params.street)
            Supplier().create(name=params.name, mobile_number=params.mobile_number,
                              email_id=params.email_id, alt_mobile_number=params.alt_mobile_number,
                              id_number=params.id_number, id_type=params.id_type,
                              gst_number=params.gst_number, photo_url=params.photo_url,
                              id_proof_url=params.id_proof_url,
                              organisation_id=token_payload.organisation_id,
                              address_id=address_id, organisation_name=token_payload.organisationName)

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(Supplier.get_all(organisation_name=token_payload.organisationName,params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        employees_utils = SupplierUtils(columns_required=params.values_list)
        data = json.loads(employees_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_extract(self, params: SuppliersGet, token_payload: Payload):
        data = Supplier.get(organisation_name=token_payload.organisationName, supplier_code=params.supplier_code)
        if len(data) == 0:
            raise ValueError(self.data_no_match)
        employees_utils = SupplierUtils(columns_required=params.values_list)
        data = json.loads(employees_utils.mapper(data=data))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: SupplierUpdate, token_payload: Payload):
        with transaction.atomic():
            supplier_data = Supplier.get(organisation_name=token_payload.organisationName,
                                         supplier_code=params.supplier_code, single=True)
            if supplier_data is None:
                raise ValueError(self.data_no_match)
            Address.update(country=params.country, street=params.street, state=params.state,
                           address_id=supplier_data['address_id'])
            Supplier.update(supplier_id=supplier_data['supplier_id'], name=params.name,
                            mobile_number=params.mobile_number, email_id=params.email_id,
                            alt_mobile_number=params.alt_mobile_number, id_number=params.id_number,
                            id_type=params.id_type, gst_number=params.gst_number, photo_url=params.photo_url,
                            id_proof_url=params.id_proof_url)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: SupplierDelete, token_payload: Payload):
        supplier = Supplier.get(organisation_name=token_payload.organisationName, supplier_code=params.supplier_code,
                                single=True)
        if supplier is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Address.remove(address_id=supplier['address_id'])
            Supplier.remove(supplier_id=supplier['supplier_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = SuppliersEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id,)
        
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: SupplierDeleteManyRequest, token_payload: Payload):
        supplier = Supplier.get_with_code_list(supplier_code=params.supplier_code,
                                               organisation_name=token_payload.organisationName)
        if len(supplier) != len(params.supplier_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(supplier)
        supplier_ids = dataframe['supplier_id'].tolist()
        address_ids = dataframe['address_id'].tolist()
        with transaction.atomic():
            Address.remove_from_list(address_id=address_ids)
            Supplier.remove_from_list(supplier_codes=supplier_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))
