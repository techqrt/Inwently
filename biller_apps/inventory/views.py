import json

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.utils import Utils
from biller_apps.inventory.dataclasses.request.get_all import InventoryGetAll
from biller_apps.inventory.models import Inventory
from biller_apps.inventory.utils import InventoryUtils

FILTER_MAPPING = {
    "name": "item_id__name",
    "branch_name": "shop_id__name",
    "item_name": "item_id__name",
}
class InventoryView():
    def __init__(self):
        self.data_get = "Data fetched successfully"
        super().__init__()
        

    @Common().exception_handler
    def get_all_extract(self, params: InventoryGetAll, token_payload: Payload):
        inventory = Inventory.get_all(organisation_name=token_payload.organisationName)
        if params.filter_key and params.filter_value:
          if params.filter_key not in FILTER_MAPPING:
           raise ValueError(Constants.invalid_filter_key)

          db_field = FILTER_MAPPING[params.filter_key]

          filter_condition = {
           f"{db_field}__icontains": params.filter_value
          }

          inventory = inventory.filter(**filter_condition)

        inventory = inventory.order_by(params.ordering)

        pages = Paginator(inventory, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        inventory_utils = InventoryUtils(columns_required=params.values_list)
        data = json.loads(inventory_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))