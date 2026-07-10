from django.urls import reverse
from rest_framework.test import APITestCase
import datetime

from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.quotations.serializers.request.create import QuotationRequest
from biller_apps.quotations.dataclasses.request.delete import QuotationDelete
from biller_apps.common.dataclasses.search import Search
from biller_apps.shops.dataclases.request.delete_many import ShopsDeleteMany
from biller_apps.quotations.serializers.request.update import QuotationUpdate
from biller_apps.quotations.serializers.request.get import QuotationGet
from biller_apps.quotations.views import QuotationView
from biller_apps.brand.models import Brand
from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation
from biller_apps.employees.models.employees import Employees
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.test_setup import TestSetUp
from biller_apps.quotations.models import Quotation



class TestViews(TestSetUp, APITestCase):
    
    def setUp(self):
        super().setUp()
        token_data = {
            "email_id": "harisjosinpeter@gmail.com",
            "expiry": "2025-02-07T17:39:44.056579",
            "organisationName": "test",
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
        quo_id = Quotation().create(
            supplier_id=self.supplier_id,
            organisation_id=self.organisation_id,
            organisation_name='test',
            item_id=self.item_id[0],
            description='Test Description',
            brand='Test Brand',
            quantity=10.0,
            price=200.0,
            tax=20.0,
            purchase=True,
            sales=False
        )
        quo_code = Quotation.objects.filter(quotation_id = quo_id).first().quotation_code
        obj = QuotationGet(quotation_code=quo_code, values='')
        resp = QuotationView().get_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        obj = QuotationRequest(supplier_id=self.supplier_id,organisation_id=self.organisation_id,total=10.0,
                           item_id=self.item_id[0],description='Test Description',brand='Test Brand',
                            quantity=10.0,price=200.0,tax=20.0,purchase=True,sales=False)
        resp = QuotationView().create_extract(params=[obj],token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        quo_id = self.quotation_id
        quo_code = Quotation.objects.filter(quotation_id = quo_id).first().quotation_code
        obj = QuotationUpdate(supplier_id=self.supplier_id,quotation_code=quo_code,organisation_id=self.organisation_id,total=10.0,
                           item_id=self.item_id[0],description='Test Description',brand='Test Brand',
                            quantity=10.0,price=200.0,tax=20.0,purchase=True,sales=False)
        resp = QuotationView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        quo_id = self.quotation_id
        quo_code = Quotation.objects.filter(quotation_id = quo_id).first().quotation_code
        obj = QuotationDelete(quotation_code=quo_code)        
        resp = QuotationView().delete_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
    def test_get_all_extract(self):
        quo_id = Quotation().create(
            supplier_id=self.supplier_id,
            organisation_id=self.organisation_id,
            organisation_name='test',
            item_id=self.item_id[0],
            description='Test Description',
            brand='Test Brand',
            quantity=10.0,
            price=200.0,
            tax=20.0,
            purchase=True,
            sales=False
        )
        quo_code = Quotation.objects.filter(quotation_id = quo_id).first().quotation_code
    
        obj = GetAll(page_num=1,limit=1,sort_by='quotation_code',sort_order='asc',values='',filter_key='purchase',filter_value=True,search_key='name')
        resp = QuotationView().get_all_extract(params=obj, token_payload=self.token_payload) 
        self.assertEqual(resp.status_code, 200)
    
    def test_search_extract(self):
        obj = Search(key="test", page_num=1, limit=10)
        resp = QuotationView().search_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)