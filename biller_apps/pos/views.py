import json

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.common.common import Common
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.organisation.models import Organisation
from biller_apps.pos.dataclasses.request.create import POSCreate
from biller_apps.pos.dataclasses.request.update import POSUpdate
from biller_apps.pos.dataclasses.request.status_change import POSStatusChange
from biller_apps.pos.dataclasses.request.get import POSGet
from biller_apps.pos.dataclasses.request.get_all import POSGetAll
from biller_apps.pos.dataclasses.request.delete import POSDelete
from biller_apps.pos.utils import POSUtils


class POSView:
    def __init__(self):
        self.data_create = "POS draft created successfully"
        self.data_update = "POS updated successfully"
        self.data_sent = "POS sent to customer"
        self.data_confirmed = "POS confirmed"
        self.data_cancelled = "POS cancelled"
        self.data_executed = "POS executed to invoice successfully"
        self.data_delete = "POS draft deleted successfully"
        self.data_get = "Data fetched successfully"

    @staticmethod
    def _resolve_organisation_id(organisation_name: str) -> int:
        organisation = Organisation.objects.filter(
            company_name=organisation_name
        ).values('organisation_id').first()
        if organisation is None:
            raise ValueError("No matching organisation found")
        return organisation['organisation_id']

    # =========================================================
    # CREATE
    # =========================================================
    # biller_apps/pos/views.py — only create_extract changes
    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: POSCreate, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        employee_id = getattr(token_payload, "employeeId", None)

        pos = POSUtils.create(
            customer_code=params.customer_code,
            shop_code=params.shop_code,
            organisation_id=organisation_id,
            organisation_name=token_payload.organisationName,
            items=params.items,
            billed_by=employee_id,
            customer_quotation_code=params.customer_quotation_code,
        )

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_create,
            data={'pos_id': pos.pos_id, 'pos_code': pos.pos_code, 'amount': str(pos.amount)}
        ))

    # =========================================================
    # UPDATE (partial replace — items + header fields)
    # =========================================================
    @Common().exception_handler
    @Publish.status_update
    def update_extract(self, params: POSUpdate, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        employee_id = getattr(token_payload, "employeeId", None)

        pos = POSUtils.update(
            pos_id=params.pos_id,
            organisation_id=organisation_id,
            items_to_add=params.items_to_add,
            items_to_update=params.items_to_update,
            items_to_remove=params.items_to_remove,
            discounts=params.discounts,
            discounts_unit=params.discounts_unit,
            wave_off=params.wave_off,
            payment_type=params.payment_type,
            billed_by=employee_id,
        )

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_update,
            data={'pos_id': pos.pos_id, 'amount': str(pos.amount)}
        ))

    # =========================================================
    # STATUS TRANSITIONS
    # =========================================================
    @Common().exception_handler
    @Publish.status_update
    def send_extract(self, params: POSStatusChange, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        employee_id = getattr(token_payload, "employeeId", None)
        pos = POSUtils.send_to_customer(pos_id=params.pos_id, organisation_id=organisation_id, sent_by=employee_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_sent, data={'pos_id': pos.pos_id, 'status': pos.status}
        ))

    @Common().exception_handler
    @Publish.status_update
    def confirm_extract(self, params: POSStatusChange, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        #employee_id = getattr(token_payload, "employeeId", None)
        pos = POSUtils.confirm(pos_id=params.pos_id, organisation_id=organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_confirmed, data={'pos_id': pos.pos_id, 'status': pos.status}
        ))

    @Common().exception_handler
    @Publish.status_update
    def cancel_extract(self, params: POSStatusChange, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        #employee_id = getattr(token_payload, "employeeId", None)
        pos = POSUtils.cancel(pos_id=params.pos_id, organisation_id=organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_cancelled, data={'pos_id': pos.pos_id, 'status': pos.status}
        ))

    # =========================================================
    # EXECUTE — final invoice step (inventory check + deduct here only)
    # =========================================================
    @Common().exception_handler
    @Publish.status_update
    def execute_extract(self, params: POSStatusChange, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        #employee_id = getattr(token_payload, "employeeId", None)

        customer_bills = POSUtils.execute_to_billing(
            pos_id=params.pos_id,
            organisation_id=organisation_id,
            organisation_name=token_payload.organisationName,
            #billed_by_id=employee_id,
        )

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_executed,
            data={
                'customer_bills_id': customer_bills.customer_bills_id,
                'bill_number': customer_bills.bill_number,
            }
        ))

    # =========================================================
    # GET
    # =========================================================
    @Common().exception_handler
    def get_extract(self, params: POSGet, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)

        pos, items = POSUtils.get(
            organisation_id=organisation_id,
            pos_id=params.pos_id,
            pos_code=params.pos_code,
        )

        data = {
            'pos_id': pos.pos_id,
            'pos_code': pos.pos_code,
            'status': pos.status,
            'payment_type': pos.payment_type,
            'payment_status': pos.payment_status,
            'discounts': str(pos.discounts),
            'discounts_unit': pos.discounts_unit,
            'wave_off': str(pos.wave_off),
            'amount': str(pos.amount),
            'customer_quotation_id': pos.customer_quotation_id,
            'items': items,
        }

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_get, data=data
        ))

    # =========================================================
    # GET ALL
    # =========================================================
    @Common().exception_handler
    def get_all_extract(self, params: POSGetAll, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)

        pos_list = POSUtils.get_all(
            organisation_id=organisation_id,
            status=params.status,
            ordering=params.ordering,
        )

        pages = Paginator(pos_list, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = list(pages.page(params.page_num))
        data = json.loads(json.dumps(data, default=str))
        data = Utils.add_page_parameter(
            final_data=data, page_num=params.page_num, present_url=token_payload.present_url,
            total_page=pages.num_pages, total_count=pages.count,
            next_page_required=pages.num_pages != params.page_num,
        )

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_get, data=data
        ))

    # =========================================================
    # DELETE (whole draft)
    # =========================================================
    @Common().exception_handler
    @Publish.status_update
    def delete_extract(self, params: POSDelete, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        POSUtils.delete(pos_id=params.pos_id, organisation_id=organisation_id)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_delete, data={}
        ))