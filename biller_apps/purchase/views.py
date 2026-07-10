import json

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import items

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.exceptions.validation_errors import ValidationErrors
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.item.models.items import Items
from biller_apps.purchase.dataclasses.request.create import PurchaseRequestDataclass, PurchaseItemsDataclass, \
    BranchSplitDataclass
from biller_apps.purchase.dataclasses.request.delete import PurchaseDelete
from biller_apps.purchase.dataclasses.request.get import PurchaseGet
from biller_apps.purchase.dataclasses.request.update import PurchaseUpdate
from biller_apps.purchase.es_query import PurchaseEsQuery
from biller_apps.purchase.models import PurchaseBills, BranchSplit
from biller_apps.purchase.models.purchase import Purchase
from biller_apps.purchase.utils import PurchaseUtils
from biller_apps.supplier.models import Supplier


class PurchaseView:
    def __init__(self):
        self.data_created = "Purchase added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Purchase deleted successfully"
        self.data_update = "Purchase updated successfully"
        self.data_no_match = "No matching purchase found"
        super().__init__()


    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: PurchaseRequestDataclass, token_payload: Payload):
        with transaction.atomic():
            purchase_bill = PurchaseBills().create(purchase_bill_number=params.purchase_bill_number,
                                                   supplier_id=params.supplier_code,
                                                   organisation_id=token_payload.organisation_id,
                                                   bill_amount=params.bill_amount,
                                                   organisation_name=token_payload.organisationName)
            for item_data in params.items:
                items = PurchaseItemsDataclass(**item_data)
                purchase_id = Purchase().create(purchase_bill=purchase_bill,item_id=items.item_code,buying_price=items.buying_price,
                                                landing_cost=items.landing_cost,selling_price=items.selling_price,tax=items.tax,
                                                quantity=items.quantity,quantity_unit=items.unit,expiry=items.expiry)
                for branches_data in items.branch_split:
                    branches = BranchSplitDataclass(**branches_data)
                    BranchSplit().create(shop=branches.branch_code,quantity=branches.quantity,purchase=purchase_id)


            return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        purchases = Purchase.get_all(organisation_name=token_payload.organisationName, params=params)
        if params.sort_by == 'name':
            params.sort_by = "purchase_bill_number"
            params.sort_order = 'asc'
            params.ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"
        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            purchases = purchases.filter(**filter_condition)

        purchases = purchases.order_by(params.ordering)

        pages = Paginator(purchases, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)
        purchase_utils = PurchaseUtils(columns_required=params.values_list)
        data = json.loads(purchase_utils.mapper(data=data))
        data = Utils.add_page_parameter(
            final_data=data,
            page_num=params.page_num,
            present_url=token_payload.present_url,
            total_page=pages.num_pages,
            total_count=pages.count,
            next_page_required=True if pages.num_pages != params.page_num else False,
        )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_extract(self, params: PurchaseGet, token_payload: Payload):
        data = Purchase.get(purchase_code=params.purchase_code, organisation_name=token_payload.organisationName)
        if not data:
            raise ValueError(self.data_no_match)

        purchase_utils = PurchaseUtils(columns_required=params.values_list)
        data = json.loads(purchase_utils.mapper(data=[data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    def update_extract(self, params: PurchaseUpdate, token_payload: Payload):
        with transaction.atomic():
            purchase_data = Purchase.get(purchase_code=params.purchase_code,
                                         organisation_name=token_payload.organisationName)
            if not purchase_data:
                raise ValueError(self.data_no_match)

            Purchase.update(
                purchase_id=purchase_data['purchase_id'],
                buying_price=params.buying_price,
                landing_cost=params.landing_cost,
                selling_price=params.selling_price,
                tax=params.tax,
                quantity=params.quantity,
                bill_amount=params.bill_amount,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    @Publish.status_update
    def delete_extract(self, params: PurchaseDelete, token_payload: Payload):
        purchase_data = Purchase.get(purchase_code=params.purchase_code,
                                     organisation_name=token_payload.organisationName)
        if not purchase_data:
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            Purchase.remove(purchase_id=purchase_data['purchase_id'])

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data= PurchaseEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
