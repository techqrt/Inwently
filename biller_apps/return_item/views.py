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
from biller_apps.common.exceptions.validation_errors import ValidationErrors
from biller_apps.common.utils import Utils
from biller_apps.return_item.dataclasses.request.create import ReturnItemRequest
from biller_apps.return_item.dataclasses.request.update import ReturnItemUpdate
from biller_apps.return_item.dataclasses.request.delete import ReturnItemDelete
from biller_apps.return_item.dataclasses.request.get import ReturnItemGet
from biller_apps.return_item.dataclasses.request.get_by_bill import ReturnItemGetByBill
from biller_apps.return_item.es_query import ReturnItemEsQuery
from biller_apps.return_item.models import ReturnItem
from biller_apps.billing.models.billing import Billing
from biller_apps.supplier.models import Supplier
from biller_apps.item.models.items import Items


class ReturnItemView:
    def __init__(self):
        self.data_created = "Return item added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Return item deleted successfully"
        self.data_update = "Return item updated successfully"
        self.data_no_match = "No matching return item found"
        super().__init__()

    # @Common().exception_handler
    def create_extract(self, params: ReturnItemRequest, token_payload: Payload):
        with transaction.atomic():
            bill_exists = Billing.objects.filter(bill_number=params.purchase_bill_number).exists()
            item_exists = Items.objects.filter(item_code=params.item_code).exists()
            supplier_exists = Supplier.objects.filter(supplier_code=params.supplier_code).exists()
            billing_id = Billing.objects.get(bill_number=params.purchase_bill_number).billing_id
            item_id = Items.objects.get(item_code=params.item_code).item_id
            supplier_id = Supplier.objects.get(supplier_code=params.supplier_code).supplier_id

            if not bill_exists:
                raise ValidationErrors(errors=[Constants.bill_not_found])
            if not item_exists:
                raise ValidationErrors(errors=[Constants.item_not_found])
            if not supplier_exists:
                raise ValidationErrors(errors=[Constants.supplier_not_found])

            total_price = ReturnItem.calculate_total_price(
                quantity=params.quantity, price=params.price, tax=params.tax
            )

            ReturnItem().create(
                bill_id=billing_id,
                supplier_id=supplier_id,
                organisation_id=token_payload.organisation_id,
                item_id=item_id,
                organisation_name=token_payload.organisationName,
                return_reason=params.return_reason,
                quantity=params.quantity,
                price=params.price,
                tax=params.tax,
            )
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(ReturnItem.get_all(organisation_name=token_payload.organisationName,params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)
        data = Utils.add_page_parameter(
            final_data=list(data),
            page_num=params.page_num,
            present_url=token_payload.present_url,
            total_page=pages.num_pages,
            total_count=pages.count,
            next_page_required=True if pages.num_pages != params.page_num else False,
        )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_extract(self, params: ReturnItemGet, token_payload: Payload):
        data = ReturnItem.get(
            return_code=params.return_code, organisation_name=token_payload.organisationName
        )
        if not data:
            raise ValueError(self.data_no_match)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
    
    @Common().exception_handler
    def get_item_by_bill_extract(self, params: ReturnItemGetByBill, token_payload: Payload):
        data = ReturnItem.get_item_by_bill(
            bill_number=params.bill_number, organisation_name=token_payload.organisationName
        )
        if not data:
            raise ValueError(self.data_no_match)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def update_extract(self, params: ReturnItemUpdate, token_payload: Payload):
        with transaction.atomic():
            return_item_data = ReturnItem.get(
                return_code=params.return_code, organisation_name=token_payload.organisationName
            )
            if not return_item_data:
                raise ValueError(self.data_no_match)

            ReturnItem.update(
                return_id=return_item_data['return_id'],
                return_reason=params.return_reason,
                quantity=params.quantity,
                price=params.price,
                tax=params.tax,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    def delete_extract(self, params: ReturnItemDelete, token_payload: Payload):
        return_item_data = ReturnItem.get(
            return_code=params.return_code, organisation_name=token_payload.organisationName
        )
        if not return_item_data:
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            ReturnItem.remove(return_id=return_item_data['return_id'])

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = ReturnItemEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id,)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
