import datetime

from future.backports.datetime import datetime, timezone

from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.serializers.request.search import Search
from biller_apps.employees.models.employees import Employees
from biller_apps.employees.serializers.request.bulk_status_change import EmployeeBulkStatusChangeRequest
from biller_apps.employees.serializers.request.create import EmployeesRequest
from biller_apps.employees.serializers.request.create import PermissionsRequestSerializer
from biller_apps.employees.serializers.request.get import EmployeeGet
from biller_apps.employees.serializers.request.update import EmployeesUpdateRequest
from biller_apps.employees.views import EmployeesView
from biller_apps.shops.models import Shops
from biller_apps.test_setup import TestSetUp


class TestViews(TestSetUp):

    def setUp(self):
        super().setUp()
        token_data = {
            "email_id": "test@gmail.com",
            "expiry": "2025-02-07T17:39:44.056579",
            "organisationName": "test",
            "organisation_id": self.organisation_id,
            "present_url": "",
            "access_token": "",
            "method": "",
            "path": "",
            "approval": False,
            "permissions": {
                "master": {
                    "item": True,
                    "shop": True,
                    "supplier": True,
                    "customer": True,
                    "create": True,
                    "employee": True
                },
                "inventory": {"inventory": True},
                "billing": {
                    "pos": True,
                    "return_item": True,
                    "bill_history": True
                },
                "reports": {
                    "general": True,
                    "overview": True,
                    "administration": True,
                    "day_book": True,
                    "gst": True
                },
                "printer_templates": {" er_templates": True},
                "dashboard": {"dashboard": True},
                "stock": {
                    "purchase_list": True,
                    "return_purchase": True,
                    "stock": True
                },
                "quotations": {"quotations": True}
            }
        }
        self.token_payload = Payload(**token_data)

    def test_get_extract(self):
        employ_code = Employees.objects.filter(organisation_id=self.organisation_id).first()
        obj = EmployeeGet(employee_code=employ_code.employee_code, values=None)
        resp = EmployeesView().get_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='is_active', sort_order='asc', filter_key='',
                     filter_value='', search_key='')
        resp = EmployeesView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        permissions_data = {
            "master": {
                "item": True,
                "shop": True,
                "supplier": True,
                "customer": True,
                "create": True,
                "employee": True
            },
            "inventory": {"inventory": True},
            "billing": {
                "pos": True,
                "return_item": True,
                "bill_history": True
            },
            "reports": {
                "general": True,
                "overview": True,
                "administration": True,
                "day_book": True,
                "gst": True
            },
            "printer_templates": {"printer_templates": True},
            "dashboard": {"dashboard": True},
            "stock": {
                "purchase_list": True,
                "return_purchase": True,
                "stock": True
            },
            "quotations": {"quotations": True}
        }
        permission = PermissionsRequestSerializer(data=permissions_data)
        permission.is_valid(raise_exception=True)
        shop_id = Shops().create(name='godzilla', organisation_id=self.organisation_id,
                                 organisation_name=self.token_payload.organisationName, address_id=self.address_id,
                                 email_id=self.token_payload.email_id, mobile_number='01010101',
                                 alt_mobile_number='01125465598', type='CUSTOM', website='test.com')
        obj = EmployeesRequest(name='testkarazuki', mobile_number='01670101', alternate_mobile_number='01005465598',
                               shop_access=['godzilla'], state='test3',
                               country='test3', street='test3', dob='2003-02-07', email_id='testkarazuki@gmail.com',
                               profile_photo_url='test/jpg', permissions=permission.validated_data)
        resp = EmployeesView().create_extract(params=obj, token_payload=self.token_payload, host='www.caddayan.com')
        self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        permissions_data = {
            "master": {
                "item": True,
                "shop": True,
                "supplier": True,
                "customer": True,
                "create": True,
                "employee": True
            },
            "inventory": {"inventory": True},
            "billing": {
                "pos": True,
                "return_item": True,
                "bill_history": True
            },
            "reports": {
                "general": True,
                "overview": True,
                "administration": True,
                "day_book": True,
                "gst": True
            },
            "printer_templates": {"printer_templates": True},
            "dashboard": {"dashboard": True},
            "stock": {
                "purchase_list": True,
                "return_purchase": True,
                "stock": True
            },
            "quotations": {"quotations": True}
        }
        permission = PermissionsRequestSerializer(data=permissions_data)
        permission.is_valid(raise_exception=True)
        employ_code = Employees.objects.filter(organisation_id=self.organisation_id).first()
        shop_access = Shops.objects.filter(organisation_id=self.organisation_id).first()
        obj = EmployeesUpdateRequest(name='test3', mobile_number='01010101', alternate_mobile_number='01125465598',
                                     state='test3', country='test3', street='test3', dob=datetime.now(tz=timezone.utc),
                                     email_id='test@gmail.com',
                                     profile_photo_url='test/jpg', employee_code=employ_code.employee_code,
                                     shop_access=[shop_access.shop_code], permissions=permission.data)

        resp = EmployeesView().update_extract(params=obj, token_payload=self.token_payload)
        print("response ", resp.data)
        self.assertEqual(resp.status_code, 200)

    def test_bulk_status_change_extract(self):
        employ_code = Employees.objects.filter(organisation_id=self.organisation_id).first()
        obj = EmployeeBulkStatusChangeRequest(employee_code=[employ_code.employee_code], status=True)
        resp = EmployeesView().bulk_status_change_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_search_extract(self):
        obj = Search(limit=10, page_num=1, key='test')
        resp = EmployeesView().search_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_get_shop_ids(self):
        shop_id = Shops().create(name='godzilla', organisation_id=self.organisation_id,
                                 organisation_name=self.token_payload.organisationName, address_id=self.address_id,
                                 email_id=self.token_payload.email_id, mobile_number='01010101',
                                 alt_mobile_number='01125465598', type='CUSTOM', website='test.com')
        resp = EmployeesView().get_shop_ids(
            shop_ids_list=list(Shops.objects.filter(shop_id=shop_id).values('shop_id', 'organisation_id_id')))
        assert len(resp) >= 0

    def test_check_constrains(self):
        obj = EmployeesRequest(name='test', mobile_number='01010101', alternate_mobile_number='01125465598',
                               shop_access=["test"], state='test3', country='test3', street='test3', dob='test',
                               email_id='test@gmail.com', profile_photo_url='test/jpg',
                               permissions=self.token_payload.permissions)
        resp = EmployeesView().check_constrains(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp, None)
