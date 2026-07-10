from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.employees.models.employees import Employees
from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops


class DashboardView:
    def __init__(self) -> None:
        super().__init__()
        self.data_fetched = "Data fetched successfully"

    def web_count(self, request: Request) -> Response:
        organisation_count = Organisation.objects.count()
        shops_count = Shops.objects.count()
        employees_count = Employees.objects.count()
        device_count = 1
        response = {'organisationCount': organisation_count, 'shopsCount': shops_count,
                    'employeesCount': employees_count, 'deviceCount': device_count}
        return Response(status=status.HTTP_200_OK, data=response)
