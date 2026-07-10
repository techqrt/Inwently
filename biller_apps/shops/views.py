import json
import urllib

import pandas
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.models.adress import Address
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.organisation.models import Organisation
from biller_apps.shops.dataclases.request.create import ShopsRequest
from biller_apps.shops.dataclases.request.delete import ShopsDelete
from biller_apps.shops.dataclases.request.delete_many import ShopsDeleteMany
from biller_apps.shops.dataclases.request.get import ShopGet
from biller_apps.shops.dataclases.request.get_all import ShopGetAll
from biller_apps.shops.dataclases.request.update import ShopsUpdateRequest
from biller_apps.shops.es_query import ShopsEsQuery
from biller_apps.shops.models import Shops
from biller_apps.shops.utils import ShopsUtils


class ShopsView:
    def __init__(self) -> None:
        self.data_created = "Shop added successfully"
        self.data_created_error_exist = "Shop name already exists"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Shop delete successfully"
        self.data_update = "Shop updated successfully"
        self.no_match = "Shop code does not exists"
        self.match_found = "Shop code exists"
        self.shop_limit_exceeded = "Shop limit exceeded"
        self.data_no_match = "Some of the shops do not exist"
        super().__init__()

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: ShopsRequest, token_payload: Payload) -> Response:
        with transaction.atomic():
            address_id = Address().create(street=params.street, state=params.state, country=params.country)
            organisation = Organisation.get(company_name=token_payload.organisationName, single=True)
            shops = Shops.get(name=params.name, organisation_id=token_payload.organisation_id, single=True)
            if shops is None:
                if Shops.get_count(organization_name=token_payload.organisationName) >= organisation['shop_count']:
                    raise ValueError(self.shop_limit_exceeded)
                shop_status = Shops().create(organisation_name=token_payload.organisationName, address_id=address_id,
                                             name=params.name, organisation_id=token_payload.organisation_id,
                                             mobile_number=params.mobile_number, email_id=params.email_id,
                                             website=params.website, alt_mobile_number=params.alt_mobile_number,
                                             type=params.type)
            else:
                raise ValueError(self.match_found)
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: ShopGetAll, token_payload: Payload) -> Response:
        pages = Paginator(Shops.get_all(organisation_name=token_payload.organisationName, type=params.type,params=params),
                          params.limit)

        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        shop_utils = ShopsUtils(columns_required=params.values_list)
        data = json.loads(shop_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url,
                                        total_page=pages.num_pages, total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: ShopsDelete, token_payload: Payload) -> Response:
        shops = Shops.get_with_code(shop_code=params.shop_code,
                                    organisation_name=urllib.parse.unquote(token_payload.organisationName))
        if shops is None:
            raise ValueError(self.no_match)
        with transaction.atomic():
            Shops.remove(shop_id=shops['shop_id'])
            Address.remove(address_id=shops['address_id_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: ShopsUpdateRequest, token_payload: Payload) -> Response:
        shop_data = Shops.get_with_code(shop_code=params.shop_code,
                                        organisation_name=urllib.parse.unquote(token_payload.organisationName))
        if shop_data is None:
            raise ValueError(self.no_match)
        with transaction.atomic():
            Address.update(state=params.state, country=params.country, street=params.street,
                           address_id=shop_data['address_id_id'])
            Shops.update(shop_id=shop_data['shop_id'], name=params.name, email_id=params.email_id,
                         mobile_number=params.mobile_number,alt_mobile_number=params.alt_mobile_number,website=params.website, type=params.type)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data= ShopsEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_many_extract(self, params: ShopsDeleteMany, token_payload: Payload):
        shops = Shops().get_with_code_list(shop_code=params.shop_code,
                                         organisation_name=token_payload.organisationName)
        if len(shops) != len(params.shop_code):
            raise ValueError(self.data_no_match)
        dataframe = pandas.DataFrame.from_records(shops)
        shop_ids = dataframe['shop_id'].tolist()
        address_ids = dataframe['address_id'].tolist()
        with transaction.atomic():
            Shops.remove_from_list(shop_id=shop_ids)
            Address.remove_from_list(address_id=address_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def get_extract(self, params: ShopGet, token_payload: Payload):
        shop_data = Shops.get_by_code(shop_code=params.shop_code)
        if len(shop_data) == 0:
            raise ValueError(self.data_no_match)
        shop_utils = ShopsUtils(columns_required=params.values_list)
        data = json.loads(shop_utils.mapper(data=shop_data))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
