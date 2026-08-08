import json

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.inventory.dataclasses.request.create import InventoryCreate
from biller_apps.inventory.dataclasses.request.get import InventoryGet
from biller_apps.inventory.dataclasses.request.get_all import InventoryGetAll
from biller_apps.inventory.dataclasses.request.update import InventoryUpdate
from biller_apps.inventory.utils import InventoryUtils
from biller_apps.organisation.models import Organisation


class InventoryView:
    def __init__(self):
        self.data_create = "Inventory added successfully"
        self.data_update = "Inventory updated successfully"
        self.data_delete = "Inventory deleted successfully"
        self.data_get = "Data fetched successfully"
        self.data_no_match_org = "No matching organisation found"
        self.data_no_match_inventory = "No matching inventory found"

    @staticmethod
    def _resolve_organisation_id(organisation_name: str) -> int:
        organisation = Organisation.objects.filter(company_name=organisation_name).values(
            'organisation_id').first()
        if organisation is None:
            raise ValueError("No matching organisation found")
        return organisation['organisation_id']

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: InventoryCreate, token_payload: Payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)

        with transaction.atomic():
            inventory = InventoryUtils.create(
                item_code=params.item_code,
                shop_code=params.shop_code,
                organisation_id=organisation_id,
                organisation_name=token_payload.organisationName,
                expiry_date=params.expiry_date,
                price=params.price,
                balance_qty=params.balance_qty,
                store_mapping=params.store_mapping,
            )

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_create, data={'inventory_id': inventory.inventory_id}))

    @Common().exception_handler
    def get_extract(self, params: InventoryGet, token_payload: Payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)

        inventory = InventoryUtils.get(
            organisation_id=organisation_id,
            inventory_id=params.inventory_id,
            inventory_code=params.inventory_code,
        )
        if inventory is None:
            raise ValueError(self.data_no_match_inventory)

        inventory_utils = InventoryUtils(columns_required=[])
        data = json.loads(inventory_utils.mapper(data=[inventory]))[0]

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    def update_extract(self, params: InventoryUpdate, token_payload: Payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)

        with transaction.atomic():
            inventory = InventoryUtils.update(
                inventory_id=params.inventory_id,
                organisation_id=organisation_id,
                item_code=params.item_code,
                shop_code=params.shop_code,
                expiry_date=params.expiry_date,
                price=params.price,
                balance_qty=params.balance_qty,
                store_mapping=params.store_mapping,
            )

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_update, data={'inventory_id': inventory.inventory_id}))

    @Common().exception_handler
    def get_all_extract(self, params: InventoryGetAll, token_payload: Payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)

        inventory = InventoryUtils.get_all(
            organisation_id=organisation_id,
            shop_code=params.shop_code or None,
            item_code=params.item_code or None,
            filter_key=params.filter_key or None,
            filter_value=params.filter_value or None,
            ordering=params.ordering,
        )

        pages = Paginator(inventory, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = list(pages.page(params.page_num))

        inventory_utils = InventoryUtils(columns_required=params.values_list)
        data = json.loads(inventory_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))