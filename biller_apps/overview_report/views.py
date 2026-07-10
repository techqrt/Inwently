from typing import List
import json
import datetime
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from biller_apps.common.publish import Publish
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller.constants import Constants
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.download import GenerateExcelPDF

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.overview_report.dataclasses.request.get_report_customer import OverviewReportCustomerGet
from biller_apps.overview_report.dataclasses.request.download import OverviewReportDownload
from biller_apps.overview_report.dataclasses.request.get_report_item import OverviewReportItemGet
from biller_apps.overview_report.dataclasses.request.get_report_supplier import OverviewReportSupplierGet
from biller_apps.common.utils import Utils
from biller_apps.overview_report.models import OverviewReport
from biller_apps.overview_report.utils import OverviewReportUtils
from biller_apps.organisation.models import Organisation
from django.http import JsonResponse


class OverviewReportView:
    def __init__(self):
        self.data_get = "Data fetched successfully"
        self.data_no_match = "No matching report found"
        super().__init__()

    @Common().exception_handler
    def get_overview_reports(self, params: OverviewReportItemGet, token_payload: Payload):
        data = OverviewReport.get_overview_reports(
            organisation_name=token_payload.organisationName,
            start_date=params.start_date,
            end_date=params.end_date
        )
        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            data = data.filter(**filter_condition)
        
        if not data:
            raise ValueError(self.data_no_match)
        
        data = data.order_by(params.ordering)

        pages = Paginator(data, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)

        overview_utils = OverviewReportUtils(columns_required=params.values_list)
        data = json.loads(overview_utils.mapper(data=data, model_type="item"))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_customer_overview_reports(self, params: OverviewReportCustomerGet, token_payload: Payload):
        data = OverviewReport.get_customer_overview_reports(
            organisation_name=token_payload.organisationName,
            start_date=params.start_date,
            end_date=params.end_date
        )

        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            data = data.filter(**filter_condition)
        
        if not data:
            raise ValueError(self.data_no_match)
        
        data = data.order_by(params.ordering)

        pages = Paginator(data, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)

        overview_utils = OverviewReportUtils(columns_required=params.values_list)
        data = json.loads(overview_utils.mapper(data=data, model_type="customer"))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def get_supplier_overview_reports(self, params:OverviewReportSupplierGet, token_payload: Payload):
        data = OverviewReport.get_supplier_overview_reports(
            organisation_name=token_payload.organisationName,
            start_date=params.start_date,
            end_date=params.end_date
        )

        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            data = data.filter(**filter_condition)
        
        if not data:
            raise ValueError(self.data_no_match)
        
        data = data.order_by(params.ordering)

        pages = Paginator(data, params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)

        overview_utils = OverviewReportUtils(columns_required=params.values_list)
        data = json.loads(overview_utils.mapper(data=data, model_type="supplier"))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
    
    def download_overview_report(self, request, params: OverviewReportDownload, token_payload: Payload):
        """Download overview report in PDF or Excel format."""
        
        report_fetcher = {
            "item": OverviewReport.get_overview_reports,
            "customer": OverviewReport.get_customer_overview_reports,
            "supplier": OverviewReport.get_supplier_overview_reports
        }

        if params.module_type not in report_fetcher:
            raise ValueError("Invalid report_type. Must be 'item', 'customer', or 'supplier'.")

        data = report_fetcher[params.module_type](
            organisation_name=token_payload.organisationName,
            start_date=params.start_date,
            end_date=params.end_date
        )

        if params.filter_key and params.filter_value:
            data = data.filter(**{params.filter_key: params.filter_value})

        if not data.exists():
            raise ValueError(self.data_no_match)

        overview_utils = OverviewReportUtils(columns_required=params.values_list)
        mapped_data = json.loads(overview_utils.mapper(data=data, model_type=params.module_type))
        data = mapped_data

        if params.download_type == "pdf":
            file_url = Common.generate_pdf(params, data)
        else:
            file_url = Common.generate_excel(params, data)
        
        return JsonResponse({"file_url": request.build_absolute_uri(file_url)})