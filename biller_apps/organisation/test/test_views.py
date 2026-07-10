from django.urls import reverse
from future.backports.datetime import datetime
from rest_framework.test import APITestCase
from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.organisation.dataclasses.request.delete_many import OrganisationDeleteManyRequest
from biller_apps.organisation.serializers.request.create import OrganisationRequest
from biller_apps.organisation.serializers.request.delete import OrganisationDelete
from biller_apps.organisation.serializers.request.get import OrganisationGet
from biller_apps.organisation.views import OrganisationViews
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.test_setup import TestSetUp


class TestViews(TestSetUp, APITestCase):
    
    def setUp(self):
        super().setUp()
        token_data = {
            "email_id": "harisjosinpeter@gmail.com",
            "expiry": "2025-02-07T17:39:44.056579",
            "organisationName": "Techaso",
            "organisation_id": 1,
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
                "printer_templates": {"printer_templates": True},
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
        obj = OrganisationGet(name='test', values='')
        resp = OrganisationViews().get_extract(params=obj)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='')
        resp = OrganisationViews().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        obj = OrganisationRequest(
            owner_name='test3', owner_mobile='01010101', name='test3', state='test3',
            country='test3', street='test3', shop_count=5, employee_count=5,
            owner_alternate_mobile='1111111111', plan='CUSTOM', plan_expiry=datetime.date(),
            owner_email='asdsdaa@gmail.com'
        )
        resp = OrganisationViews().create_extract(params=obj)
        self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        obj = OrganisationRequest(
            owner_name='test3', owner_mobile='01010101', name='test3', state='test3',
            country='test3', street='test3', shop_count=5, employee_count=5,
            owner_alternate_mobile='1111111011', plan='CUSTOM', plan_expiry=datetime.date(),
            owner_email='asdsdaa@gmail.com'
        )
        OrganisationViews().create_extract(params=obj)
        resp = OrganisationViews().update_extract(params=obj)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        obj = OrganisationDelete(name='test')
        resp = OrganisationViews().delete_extract(params=obj)
        self.assertEqual(resp.status_code, 200)
    
    def test_delete_many_extract(self):
        obj = OrganisationDeleteManyRequest(organisation_id=[2])
        resp = OrganisationViews().delete_many_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
