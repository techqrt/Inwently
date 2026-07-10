import json

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.approvals.dataclasses.request.get_all import ApprovalsGetAllRequest
from biller_apps.approvals.dataclasses.request.status_change import ApprovalsStatusChangeRequest
from biller_apps.approvals.models import Approvals
from biller_apps.approvals.utils import ApproverUtils
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.reverse_call import ReverseCall
from biller_apps.common.utils import Utils


class ApproverViews:
    def __init__(self):
        self.data_get = "Data fetched successfully"
        self.approval_code_not_found = "No data found"
        self.data_approved = "Request approved successfully"
        self.data_approve_error = "Failed to approve the request"

    @Common().exception_handler
    def get_all_unapproved_extract(self, params: ApprovalsGetAllRequest, token_payload: Payload):
        pages = Paginator(Approvals.get_all_unapproved(organisation_name=token_payload.organisationName), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        customer_utils = ApproverUtils(columns_required=params.values_list)
        data = json.loads(customer_utils.mapper(data=data))
        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url, total_page=pages.num_pages,
                                        total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.data_get, data=data))

    @Common().exception_handler
    def status_change_extract(self, params: ApprovalsStatusChangeRequest, token_payload: Payload):
        approver_data = Approvals.get_by_code(approver_code=params.approval_code,
                                              organisation_name=token_payload.organisationName)
        if approver_data is None:
            raise ValueError(self.approval_code_not_found)
        res = ReverseCall(url_name=approver_data['url_name'],
                          data=json.loads(approver_data['payload']),
                          payload=token_payload).delete()

        if res.status_code == status.HTTP_200_OK:
            Response(status=res.status_code, data=Utils.success_response_data(message=self.data_approved))
        return Response(status=res.status_code,
                        data=Utils.error_response_data(message=self.data_approve_error, error=[res.json()['message']]))
