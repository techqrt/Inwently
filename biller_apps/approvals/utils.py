import json
from dataclasses import asdict

import pandas
from django.db import transaction
from django.urls import resolve
from rest_framework import status
from rest_framework.response import Response

from biller_apps.approvals.models import Approvals
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
from biller_apps.common.utils import Utils


class ApproverUtils:
    def __init__(self, columns_required: list) -> None:
        self.columns_required = columns_required
        self.mapped_column_names = {
            'request_from': 'requestFrom',
            'request_method': 'requestMethod',
            'payload': 'payload',
            'approval_code': 'approvalCode'

        }

    def mapper(self, data: list) -> list | None | str:
        if len(data) == 0:
            return '[]'
        dataframe = pandas.DataFrame.from_records(data)
        dataframe.rename(columns=self.mapped_column_names, inplace=True)

        if len(self.columns_required) == 0:
            return dataframe.to_json(orient='records')
        else:
            Common.mapper_value_error(mapped_column_names=self.mapped_column_names,
                                      columns_required=self.columns_required)

        dataframe = dataframe[self.columns_required]
        return dataframe.to_json(orient='records')

    @staticmethod
    def approver(func):
        def check(*args, **kwargs):
            params = kwargs['params']
            payload: Payload = kwargs['token_payload']
            if payload.approval:
                with transaction.atomic():
                    approval_id = Approvals().create(organisation_id=payload.organisation_id,
                                                     request_from=payload.email_id,
                                                     url_name=resolve(payload.path).url_name,
                                                     request_method=payload.method,
                                                     payload=json.dumps(asdict(params)),
                                                     organisation_name=payload.organisationName)
                return Response(status=status.HTTP_202_ACCEPTED,
                                data=Utils.success_response_data(message="Request has been created for approval",
                                                                 data={'approverRequestId': approval_id}))
            return func(*args, **kwargs)

        return check
