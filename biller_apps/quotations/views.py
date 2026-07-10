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
from biller_apps.quotations.dataclasses.request.create import QuotationRequest
from biller_apps.quotations.dataclasses.request.update import QuotationUpdate
from biller_apps.quotations.dataclasses.request.delete import QuotationDelete
from biller_apps.quotations.dataclasses.request.get import QuotationGet
from biller_apps.quotations.es_query import QuotationEsQuery
from biller_apps.quotations.models import Quotation
from biller_apps.quotations.utils import QuotationUtils
from biller_apps.supplier.models import Supplier
from biller_apps.item.models.items import Items


class QuotationView:
    def __init__(self):
        self.data_created = "Quotation added successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Quotation deleted successfully"
        self.data_update = "Quotation updated successfully"
        self.data_no_match = "No matching quotation found"
        super().__init__()

    @Common().exception_handler
    def create_extract(self, params: list[QuotationRequest], token_payload: Payload):
        with transaction.atomic():
            for param in params:
                supplier_exists = Supplier.objects.filter(supplier_id=param.supplier_id).exists()
                item_exists = Items.objects.filter(item_id=param.item_id).exists()

                if not supplier_exists:
                    raise ValidationErrors(errors=[Constants.supplier_not_found])
                if not item_exists:
                    raise ValidationErrors(errors=[Constants.item_not_found])

                total_price = Quotation.calculate_total_price(price=param.price, tax=param.tax, quantity=param.quantity)

                Quotation().create(
                    supplier_id=param.supplier_id,
                    organisation_id=token_payload.organisation_id,
                    organisation_name=token_payload.organisationName,
                    item_id=param.item_id,
                    description=param.description,
                    brand=param.brand,
                    quantity=param.quantity,
                    price=param.price,
                    tax=param.tax,
                    purchase=param.purchase,
                    sales=param.sales,
                )
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload):
        pages = Paginator(Quotation.get_all(organisation_name=token_payload.organisationName,params=params), params.limit)
        
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)
        quotation_utils = QuotationUtils(columns_required=params.values_list)
        data = json.loads(quotation_utils.mapper(data=data))
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
    def get_extract(self, params: QuotationGet, token_payload: Payload):
        data = Quotation.get(quotation_code=params.quotation_code, organisation_name=token_payload.organisationName)
        if not data:
            raise ValueError(self.data_no_match)

        quotation_utils = QuotationUtils(columns_required=params.values_list)
        data = json.loads(quotation_utils.mapper(data=[data]))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def update_extract(self, params: QuotationUpdate, token_payload: Payload):
        with transaction.atomic():
            quotation_data = Quotation.get(quotation_code=params.quotation_code, organisation_name=token_payload.organisationName)
            if not quotation_data:
                raise ValueError(self.data_no_match)

            Quotation.update(
                quotation_id=quotation_data['quotation_id'],
                description=params.description,
                brand=params.brand,
                quantity=params.quantity,
                price=params.price,
                tax=params.tax,
                purchase=params.purchase,
                sales=params.sales,
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    def delete_extract(self, params: QuotationDelete, token_payload: Payload):
        quotation_data = Quotation.get(quotation_code=params.quotation_code, organisation_name=token_payload.organisationName)
        if not quotation_data:
            raise ValueError(self.data_no_match)

        with transaction.atomic():
            Quotation.remove(quotation_id=quotation_data['quotation_id'])

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = QuotationEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
