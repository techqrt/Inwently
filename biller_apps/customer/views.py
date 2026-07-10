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
from biller_apps.customer.dataclasses.request.create import CustomerRequest
from biller_apps.customer.dataclasses.request.delete_many import CustomerDeleteManyRequest
from biller_apps.customer.dataclasses.request.get import CustomerGet
from biller_apps.customer.es_query import CustomerEsQuery
from biller_apps.customer.models import Customer
from biller_apps.customer.serializers.request.delete import CustomerDelete
from biller_apps.customer.serializers.request.update import CustomerUpdateRequest
from biller_apps.customer.utils import CustomerUtils


class CustomerView:
    def __init__(self):
        self.data_created = "Customer added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Customer delete successfully"
        self.data_update = "Customer updated successfully"
        self.data_no_match = "No matching Customer found"

    @staticmethod
    def unique_validator(mobile_number: str, email_id: str, organisation_name: str):
        mob_unique = CustomerUtils.check_uniqueness(key='mobile_number', value=mobile_number,
                                                    organisation_name=organisation_name)
        email_unique = CustomerUtils.check_uniqueness(key='email_id', value=email_id,
                                                      organisation_name=organisation_name)
        errors = []
        if mob_unique is not None:
            errors.append(Constants.mobile_number_not_unique)
        if email_unique is not None:
            errors.append(Constants.email_id_not_unique)
        if len(errors) > 0:
            raise ValidationErrors(errors=errors)

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: CustomerRequest, token_payload: Payload):
        with transaction.atomic():
            self.unique_validator(mobile_number=params.mobile_number, email_id=params.email_id,
                                  organisation_name=token_payload.organisationName)
            address_id = Address().create(state=params.state, country=params.country, street=params.street)
            Customer().create(name=params.name, mobile_number=params.mobile_number, email_id=params.email_id,
                              id_number=params.id_number, id_type=params.id_type, photo_url=params.photo_url,
                              id_proof_url=params.id_proof_url, organisation_name=token_payload.organisationName,
                              address_id=address_id, organisation_id=token_payload.organisation_id,
                              blood_group=params.blood_group, date_of_birth=params.date_of_birth,
                              education=params.education, gender=params.gender, martial_status=params.martial_status,
                              occupation=params.occupation, religion=params.religion)

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(Customer.get_all(organisation_name=token_payload.organisationName,params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        customer_utils = CustomerUtils(columns_required=params.values_list)
        data = json.loads(customer_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_extract(self, params: CustomerGet, token_payload: Payload):
        data = Customer.get(organisation_name=token_payload.organisationName, customer_code=params.customer_code)

        if len(data) == 0:
            raise ValueError(self.data_no_match)
        customer_utils = CustomerUtils(columns_required=params.values_list)

        data = json.loads(customer_utils.mapper(data=data))[0]

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: CustomerUpdateRequest, token_payload: Payload):
        with transaction.atomic():
            customer_data = Customer.get(organisation_name=token_payload.organisationName,
                                         customer_code=params.customer_code, single=True)
            if customer_data is None:
                raise ValueError(self.data_no_match)
            Address.update(country=params.country, street=params.street, state=params.state,
                           address_id=customer_data['address_id'])
            Customer.update(customer_id=customer_data['customer_id'], name=params.name,
                            mobile_number=params.mobile_number, email_id=params.email_id, id_number=params.id_number,
                            id_type=params.id_type, photo_url=params.photo_url, id_proof_url=params.id_proof_url,
                            blood_group=params.blood_group, date_of_birth=params.date_of_birth,
                            education=params.education, gender=params.gender, martial_status=params.martial_status,
                            occupation=params.occupation, religion=params.religion)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: CustomerDelete, token_payload: Payload):
        customer = Customer.get(organisation_name=token_payload.organisationName, customer_code=params.customer_code,
                                single=True)
        if customer is None:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            Address.remove(address_id=customer['address_id'])
            Customer.remove(customer_id=customer['customer_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = CustomerEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: CustomerDeleteManyRequest, token_payload: Payload):
        customer = Customer.get_with_code_list(customer_code=params.customer_code,
                                               organisation_name=token_payload.organisationName)
        if len(customer) != len(params.customer_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(customer)
        customer_ids = dataframe['customer_id'].tolist()
        address_ids = dataframe['address_id'].tolist()
        with transaction.atomic():
            Customer.remove_from_list(customer_id=customer_ids)
            Address.remove_from_list(address_id=address_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))
