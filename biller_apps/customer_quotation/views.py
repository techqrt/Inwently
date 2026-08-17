# biller_apps/customer_quotation/views.py
from rest_framework import status
from rest_framework.response import Response 

from biller_apps.common.common import Common
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.organisation.models import Organisation
from biller_apps.customer_quotation.utils import CustomerQuotationUtils


class CustomerQuotationView:
    def __init__(self):
        self.data_create = "Quotation submitted successfully"
        self.data_review = "Quotation reviewed successfully"
        self.data_get = "Data fetched successfully"

    @staticmethod
    def _resolve_organisation_id(organisation_name: str) -> int:
        organisation = Organisation.objects.filter(company_name=organisation_name).values(
            'organisation_id').first()
        if organisation is None:
            raise ValueError("No matching organisation found")
        return organisation['organisation_id']

    

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        quotation = CustomerQuotationUtils.create(
            customer_name=params.customer_name,
            customer_phone=params.customer_phone,
            customer_email=params.customer_email,
            shop_code=params.shop_code,
            items=params.items,
            organisation_id=organisation_id,
            organisation_name=token_payload.organisationName,
        )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_create,
            data={'customer_quotation_id': quotation.customer_quotation_id,
                  'customer_quotation_code': quotation.customer_quotation_code}))

    @Common().exception_handler
    @Publish.status_update
    def review_extract(self, params, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        employee_id = getattr(token_payload, "employeeId", None)
        quotation = CustomerQuotationUtils.review(
            customer_quotation_id=params.customer_quotation_id,
            organisation_id=organisation_id,
            status=params.status,
            reviewed_by_id=employee_id,
        )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_review, data={'customer_quotation_id': quotation.customer_quotation_id,
                                             'status': quotation.status}))
    
    @Common().exception_handler
    def get_extract(self, params, token_payload):
        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        quotation, items = CustomerQuotationUtils.get(
            organisation_id=organisation_id,
            customer_quotation_id=params.customer_quotation_id,
            customer_quotation_code=params.customer_quotation_code,
        )
        data = {
            'customer_quotation_id': quotation.customer_quotation_id,
            'customer_quotation_code': quotation.customer_quotation_code,
            'customer_name': quotation.customer_name,
            'customer_phone': quotation.customer_phone,
            'status': quotation.status,
            'items': items,
        }
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_get, data=data))

    @Common().exception_handler
    def get_all_extract(self, params, token_payload):
        import json
        from django.core.paginator import Paginator
        from biller.constants import Constants

        organisation_id = self._resolve_organisation_id(token_payload.organisationName)
        quotations = CustomerQuotationUtils.get_all(
            organisation_id=organisation_id, status=params.status, ordering=params.ordering,
        )
        pages = Paginator(quotations, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = list(pages.page(params.page_num))
        data = json.loads(json.dumps(data, default=str))
        data = CustomerQuotationUtils.add_page_parameter(
            final_data=data, page_num=params.page_num, present_url=token_payload.present_url,
            total_page=pages.num_pages, total_count=pages.count,
            next_page_required=pages.num_pages != params.page_num,
        )
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(
            message=self.data_get, data=data))