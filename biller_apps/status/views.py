from dataclasses import asdict

from rest_framework import status
from rest_framework.response import Response

from biller_apps.common.common import Common
from biller_apps.common.utils import Utils
from biller_apps.status.dataclasses.response.get import StatusGetResponse
from biller_apps.status.models import Status
from biller_apps.status.serializers.request.get import StatusGet


class StatusView:
    def __init__(self):
        self.data_get = "Data fetched successfully"
        super().__init__()

    @Common().exception_handler
    def get_extract(self, params: StatusGet):
        status_data = Status.get(status_id=params.status_id)
        if status_data is None:
            data = StatusGetResponse(statusId=params.status_id, status='Not started', progress=0)
        else:
            data = StatusGetResponse(statusId=status_data['uuid'], status=status_data['status'],
                                     progress=status_data['progress'])

        return Response(status=status.HTTP_200_OK,
                        data=Utils.success_response_data(message=self.data_get, data=asdict(data)))
