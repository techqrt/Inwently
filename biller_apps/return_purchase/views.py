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
from biller_apps.return_purchase.dataclasses.request.create import ReturnPurchaseRequest
from biller_apps.return_purchase.dataclasses.request.update import ReturnPurchaseUpdate
from biller_apps.return_purchase.dataclasses.request.delete import ReturnPurchaseDelete
from biller_apps.return_purchase.dataclasses.request.get import ReturnPurchaseGet
from biller_apps.return_purchase.es_query import ReturnPurchaseEsQuery
from biller_apps.return_purchase.models import ReturnPurchase
from biller_apps.return_purchase.utils import ReturnPurchaseUtils
from biller_apps.purchase.models.purchase import Purchase
from biller_apps.supplier.models import Supplier
from biller_apps.item.models.items import Items


class ReturnPurchaseView:
    def __init__(self):
        self.data_created = "Return purchase added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Return purchase deleted successfully"
        self.data_update = "Return purchase updated successfully"
        self.data_no_match = "No matching return purchase found"
        super().__init__()

    @Common().exception_handler
    def create_extract(self, params: list[ReturnPurchaseRequest], token_payload: Payload):
        with transaction.atomic():
            for param in params:
                purchase_exists = Purchase.objects.filter(purchase_id=param.purchase_id).exists()
                supplier_exists = Supplier.objects.filter(supplier_id=param.supplier_id).exists()
                item_exists = Items.objects.filter(item_id=param.item_id).exists()

                if not purchase_exists:
                    raise ValidationErrors(errors=[Constants.purchase_not_found])
                if not supplier_exists:
                    raise ValidationErrors(errors=[Constants.supplier_not_found])
                if not item_exists:
                    raise ValidationErrors(errors=[Constants.item_not_found])

                total_price = ReturnPurchase.calculate_total_price(quantity=param.quantity, tax=param.tax)

                ReturnPurchase().create(
                    purchase_id=param.purchase_id,
                    supplier_id=param.supplier_id,
                    organisation_id=token_payload.organisation_id,
                    item_id=param.item_id,
                    organisation_name=token_payload.organisationName,
                    return_reason=param.return_reason,
                    quantity=param.quantity,
                    tax=param.tax,
                    total_price=total_price,
                )
            return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(ReturnPurchase.get_all(organisation_name=token_payload.organisationName, params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)
        return_purchase_utils = ReturnPurchaseUtils(columns_required=params.values_list)
        data = json.loads(return_purchase_utils.mapper(data=data))
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
    def get_extract(self, params: ReturnPurchaseGet, token_payload: Payload):
        data = ReturnPurchase.get(return_code=params.return_code, organisation_name=token_payload.organisationName)
        if not data:
            raise ValueError(self.data_no_match)

        return_purchase_utils = ReturnPurchaseUtils(columns_required=params.values_list)
        data = json.loads(return_purchase_utils.mapper(data=[data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def update_extract(self, params: ReturnPurchaseUpdate, token_payload: Payload):
        with transaction.atomic():
            return_purchase_data = ReturnPurchase.get(return_code=params.return_code, organisation_name=token_payload.organisationName)
            if not return_purchase_data:
                raise ValueError(self.data_no_match)

            ReturnPurchase.update(
                return_id=return_purchase_data['return_id'],
                return_reason=params.return_reason,
                quantity=params.quantity,
                tax=params.tax,
                total_price=params.total_price,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    def delete_extract(self, params: ReturnPurchaseDelete, token_payload: Payload):
        return_purchase_data = ReturnPurchase.get(return_code=params.return_code, organisation_name=token_payload.organisationName)
        if not return_purchase_data:
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            ReturnPurchase.remove(return_id=return_purchase_data['return_id'])

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = ReturnPurchaseEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
