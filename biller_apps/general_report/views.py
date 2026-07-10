from typing import List
import json
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from biller_apps.common.publish import Publish
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller.constants import Constants
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.utils import Utils
from biller_apps.general_report.models import GeneralReport
from biller_apps.general_report.dataclasses.request.get_report import GeneralReportGet
from biller_apps.general_report.utils import GeneralReportUtils
from biller_apps.organisation.models import Organisation


class GeneralReportView:
    def __init__(self):
        self.data_get = "Data fetched successfully"
        self.data_no_match = "No matching report found"
        super().__init__()

    @Common().exception_handler
    def get_purchase_reports(self, params: GeneralReportGet, token_payload: Payload):
        data = GeneralReport.get_purchase_reports(
            organisation_name=token_payload.organisationName,
            start_date=params.start_date,
            end_date=params.end_date
        )

        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            data = data.filter(**filter_condition)
        
        if not data:
            raise ValueError(self.data_no_match)
        
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=list(data)))

    @Common().exception_handler
    def get_quotation_reports(self, params: GeneralReportGet, token_payload: Payload):
        data = GeneralReport.get_quotation_reports(
            organisation_name=token_payload.organisationName,
            start_date=params.start_date,
            end_date=params.end_date
        )
        
        if params.filter_key and params.filter_value:
            filter_condition = {params.filter_key: params.filter_value}
            data = data.filter(**filter_condition)
        
        if not data:
            raise ValueError(self.data_no_match)
        

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=list(data)))
