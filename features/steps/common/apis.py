from django.test import Client

from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation

from features.steps.common.constants import Constants
from features.steps.common.endpoints import Endpoints

from django.utils import timezone

from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees
from biller_apps.employees.models.permission import SalesPermission, PrinterTemplatesPermission, ReportsPermission, \
    PurchasePermission, DashboardPermission, InventoryPermission, MasterDataPermission, QuotationsPermission

class Apis:


    def __init__(self):
        self.client = Client()
        self.load_tokens()



    def post_api(self, url: str, data: dict = None, headers=None):
        return self.client.post(url, data, content_type="application/json", headers=headers)


    def get_api(self, url: str, param: dict = None, headers=None):
        return self.client.get(url, query_params=param, headers=headers)


    def delete_api(self, url: str, data: dict = None, headers=None):
        return self.client.delete(url, query_params=data, content_type="application/json", headers=headers)


    def patch_api(self, url: str, data: dict = None, headers=None):
        return self.client.patch(url, data, content_type="application/json", headers=headers)


    def put_api(self, url: str, data: dict = None, headers=None):
        return self.client.put(url, data=data, content_type="application/json", headers=headers)

    def load_tokens(self):
        sales_id = SalesPermission().create(pos=True, return_item=True, bill_history=True)
        printer_template_id = PrinterTemplatesPermission().create(printer_templates=True)
        reports_id = ReportsPermission().create(general=True, overview=True, administration=True, day_book=True,
                                                gst=True)
        purchase_id = PurchasePermission().create(purchase_list=True, return_purchase=True, stock=True)
        dashboard_id = DashboardPermission().create(dashboard=True)
        inventory_id = InventoryPermission().create(inventory=True)
        master_id = MasterDataPermission().create(item=True, supplier=True, shop=True, customer=True, employee=True,
                                                  create=True)
        quotation_id = QuotationsPermission().create(quotations=True)

        credential_id = EmployeeCredentials().create(email_id="admin1@caddayn.org", password="123456789", secure=True)
        address_id = Address().create(state="test", country="test", street="test")
        address_id2 = Address().create(state="test", country="test", street="test")
        org_id = Organisation().create(company_name="test", owner_name="test", owner_mobile="test", owner_alternate_mobile="test", address_id=address_id2,shop_count=5, employee_count=5, owner_email="test@1234.com")
        Employees.objects.create(employee_id=10, name="admin", mobile_number="03421221312", alternate_mobile_number="01231212",
                                 dob="2020-01-01",
                                 shop_access=[], address_id_id=address_id,
                                 employee_credentials_id_id=credential_id, organisation_id_id=org_id,
                                 profile_photo_url="", is_active=True, secure=True,
                                 dashboard_permission_id=dashboard_id,
                                 master_data_permission_id=master_id, inventory_permission_id=inventory_id,
                                 sales_permission_id=sales_id, quotations_permission_id=quotation_id,
                                 printer_templates_permission_id=printer_template_id,
                                 purchase_permission_id=purchase_id,
                                 reports_permission_id=reports_id, token_key="test", refresh_token="test", otp=123456,
                                 otp_expiry=timezone.now() + timezone.timedelta(minutes=10), employee_code="T_10")
        url = Endpoints.login
        response = self.client.post(url, {
            "email_id": Constants.global_username,
            "password": Constants.global_password
        }, content_type="application/json").json()

        response_data = response.get("data", {})

        self.access_token = response_data.get("access_token", None)
        self.refresh_token = response_data.get("refresh_token", None)
