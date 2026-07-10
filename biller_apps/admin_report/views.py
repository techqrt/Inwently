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
from biller_apps.admin_report.dataclasses.request.get_employee_report import AdminReportEmployeeGet
from biller_apps.common.utils import Utils
from biller_apps.admin_report.models import AdminReport
from biller_apps.admin_report.utils import AdminReportUtils
from biller_apps.organisation.models import Organisation
from django.http import JsonResponse


class AdminReportView:
    def __init__(self):
        self.data_get = "Data fetched successfully"
        self.data_no_match = "No matching report found"
        super().__init__()

    @Common().exception_handler
    def get_admin_reports(self, params: AdminReportEmployeeGet, token_payload: Payload):
        data = AdminReport.get_admin_reports(
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

        admin_utils = AdminReportUtils(columns_required=params.values_list)
        data = json.loads(admin_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))
