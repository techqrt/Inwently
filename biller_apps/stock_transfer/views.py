from typing import List
import json
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.common.publish import Publish

from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller.constants import Constants
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.exceptions.validation_errors import ValidationErrors
from biller_apps.common.utils import Utils
from biller_apps.stock_transfer.dataclasses.request.create import StockTransferRequest
from biller_apps.stock_transfer.dataclasses.request.update import StockTransferUpdate
from biller_apps.stock_transfer.dataclasses.request.get import StockTransferGet
from biller_apps.stock_transfer.dataclasses.request.delete import StockTransferDelete
from biller_apps.stock_transfer.es_query import StockTransfersEsQuery
from biller_apps.stock_transfer.models import StockTransfer
from biller_apps.stock_transfer.utils import StockTransferUtils
from biller_apps.shops.models import Shops
from biller_apps.item.models.items import Items

class StockTransferView:
    def __init__(self):
        self.data_created = "Stock transfer request created successfully"
        self.data_get = "Data fetched successfully"
        self.data_delete = "Stock transfer delete successfully"
        self.data_update = "Stock transfer updated successfully"
        self.data_no_match = "No matching stock transfer found"
        super().__init__()

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: List[StockTransferRequest], token_payload: Payload):
        with transaction.atomic():
            for transfer_request in params:
                source_shop = Shops.objects.get(shop_code=transfer_request.source_shop_code).shop_id
                destination_shop = Shops.objects.get(shop_code=transfer_request.destination_shop_code).shop_id
                item = Items.objects.get(item_code=transfer_request.item_code).item_id

                if not source_shop or not destination_shop or not item:
                    raise ValueError(self.data_no_match)

                StockTransfer().create(
                    source_shop_id=source_shop,
                    destination_shop_id=destination_shop,
                    item_id=item,
                    quantity=transfer_request.quantity,
                    organisation_id=token_payload.organisation_id,
                    remarks=transfer_request.remarks,
                    requested_by=token_payload.email_id,
                    organisation_name=token_payload.organisationName,
                )

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))

    @Common().exception_handler
    def get_extract(self, params: StockTransferGet, token_payload: Payload):
        data = StockTransfer.get(organisation_name=token_payload.organisationName, transfer_code=params.transfer_code)
        if len(data) == 0:
            raise ValueError(self.data_no_match)
        employees_utils = StockTransferUtils(columns_required=params.values_list)
        data = json.loads(employees_utils.mapper(data=data))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
    
    @Common().exception_handler
    def get_pending_transfers(self, params: GetAll, token_payload: Payload):
        transfers = StockTransfer.get_pending_transfers(organisation_name=token_payload.organisationName)

        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            transfers = transfers.filter(**filter_condition)

        if params.sort_by == 'name':
            params.sort_by = 'requested_by'
            ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"

        transfers = transfers.order_by(ordering)


        pages = Paginator(transfers, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)


        transfers_utils = StockTransferUtils(columns_required=params.values_list)
        data = json.loads(transfers_utils.mapper(data=data))


        data = Utils.add_page_parameter(
            final_data=data,
            page_num=params.page_num,
            present_url=token_payload.present_url,
            total_page=pages.num_pages,
            total_count=pages.count,
            next_page_required=True if pages.num_pages != params.page_num else False
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common().exception_handler
    def get_completed_transfers(self, params: GetAll, token_payload: Payload):

        transfers = StockTransfer.get_completed_transfers(organisation_name=token_payload.organisationName)


        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            transfers = transfers.filter(**filter_condition)

        if params.sort_by == 'name':
            params.sort_by = 'requested_by'
            params.ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"

        transfers = transfers.order_by(params.ordering)


        pages = Paginator(transfers, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)


        transfers_utils = StockTransferUtils(columns_required=params.values_list)
        data = json.loads(transfers_utils.mapper(data=data))


        data = Utils.add_page_parameter(
            final_data=data,
            page_num=params.page_num,
            present_url=token_payload.present_url,
            total_page=pages.num_pages,
            total_count=pages.count,
            next_page_required=True if pages.num_pages != params.page_num else False
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )

    @Common().exception_handler
    def get_rejected_transfers(self, params: GetAll, token_payload: Payload):
        transfers = StockTransfer.get_rejected_transfers(organisation_name=token_payload.organisationName)

        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            transfers = transfers.filter(**filter_condition)

        if params.sort_by == 'name':
            params.sort_by = 'requested_by'
            params.ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"

        transfers = transfers.order_by(params.ordering)

        pages = Paginator(transfers, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)

        data = pages.page(params.page_num)


        transfers_utils = StockTransferUtils(columns_required=params.values_list)
        data = json.loads(transfers_utils.mapper(data=data))


        data = Utils.add_page_parameter(
            final_data=data,
            page_num=params.page_num,
            present_url=token_payload.present_url,
            total_page=pages.num_pages,
            total_count=pages.count,
            next_page_required=True if pages.num_pages != params.page_num else False
        )

        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.data_get, data=data)
        )



    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def update_extract(self, params: StockTransferUpdate, token_payload: Payload):
        with transaction.atomic():
            transfer_data = StockTransfer.get(organisation_name=token_payload.organisationName, transfer_id=params.transfer_id)
            if not transfer_data:
                raise ValueError(self.data_no_match)

            StockTransfer.update(
                transfer_id=params.transfer_id,
                status=params.status,
                approved_by=token_payload.username,
                remarks=params.remarks
            )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_update))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data= StockTransfersEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    @Publish.status_update
    @ApproverUtils.approver
    def delete_extract(self, params: StockTransferDelete, token_payload: Payload):
        transfer = StockTransfer.get(organisation_name=token_payload.organisationName, transfer_code=params.transfer_code)
        if not transfer:
            raise ValueError(self.data_no_match)
        with transaction.atomic():
            StockTransfer.remove(transfer_id=transfer['transfer_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_delete))
