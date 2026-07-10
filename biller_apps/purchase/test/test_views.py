from django.urls import reverse
from rest_framework.test import APITestCase
import datetime

from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.purchase.serializers.request.create import PurchaseRequest
from biller_apps.purchase.dataclasses.request.delete import PurchaseDelete
from biller_apps.purchase.serializers.request.update import PurchaseUpdate
from biller_apps.purchase.serializers.request.get import PurchaseGet
from biller_apps.purchase.views import PurchaseView
from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.supplier.models import Supplier
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.test_setup import TestSetUp
from biller_apps.purchase.models import Purchase
from biller_apps.item.models.items import Items




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
        purchase_id =  Purchase(purchase_id=10).create(
            purchase_bill_number=self.bill_number,
            supplier_id=1,
            item_id=self.item_id[0],
            buying_price=100.0,
            organisation_id=1,
            organisation_name='Test Organisation',
            landing_cost=110.0,
            selling_price=150.0,
            tax=10.0,
            quantity=5.0,
            bill_amount=550.0
        )
        purchase_code = Purchase.objects.filter(purchase_id=purchase_id).first().purchase_code
        obj = PurchaseGet(purchase_code=purchase_code,values='')
        resp = PurchaseView().get_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='',search_key='')
        resp = PurchaseView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        purchase_id =  Purchase(purchase_id=11).create(
            purchase_bill_number=self.bill_number,
            supplier_id=1,
            item_id=self.item_id[0],
            buying_price=100.0,
            organisation_id=1,
            organisation_name='Test Organisation',
            landing_cost=110.0,
            selling_price=150.0,
            tax=10.0,
            quantity=5.0,
            bill_amount=550.0
        )
        item_code = Items.objects.filter(item_id=self.item_id[0]).first().item_code
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        obj = PurchaseRequest(purchase_bill_number=self.bill_number,supplier_code=supplier_code,item_code=item_code,buying_price=100.0,
                            landing_cost=110.0,selling_price=150.0,tax=10.0,quantity=5.0,bill_amount=550.0)
        resp = PurchaseView().create_extract(params=[obj],token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        item_id = self.item_id[0]
        bill_number = self.bill_number
        purchase_id =  Purchase(purchase_id=11).create(
            purchase_bill_number=bill_number,
            supplier_id=1,
            item_id=item_id,
            buying_price=100.0,
            organisation_id=1,
            organisation_name='Test Organisation',
            landing_cost=110.0,
            selling_price=150.0,
            tax=10.0,
            quantity=5.0,
            bill_amount=550.0
        )
        purchase_code = Purchase.objects.filter(purchase_id=purchase_id).first().purchase_code
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        supplier_code = Supplier.objects.filter(supplier_id=1).first().supplier_code 
        obj = PurchaseUpdate(purchase_bill_number=bill_number,supplier_code=supplier_code,item_code=item_code,buying_price=100.0,
                            landing_cost=110.0,selling_price=150.0,tax=10.0,quantity=5.0,bill_amount=550.0,purchase_code=purchase_code)

        resp = PurchaseView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        item_id = self.item_id[0]
        bill_number = self.bill_number
        organisation_id = self.organisation_id
        purchase_id =  Purchase(purchase_id=15).create(
            purchase_bill_number=bill_number,
            supplier_id=1,
            item_id=item_id,
            buying_price=100.0,
            organisation_id=1,
            organisation_name='Test2',
            landing_cost=110.0,
            selling_price=150.0,
            tax=10.0,
            quantity=5.0,
            bill_amount=550.0
        )
        purchase_code = Purchase.objects.filter(purchase_id=purchase_id).first().purchase_code
        obj = PurchaseDelete(purchase_code=purchase_code)
        resp = PurchaseView().delete_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
