from django.urls import reverse
from rest_framework.test import APITestCase
import datetime

from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.return_item.dataclasses.request.get_by_bill import ReturnItemGetByBill
from biller_apps.return_item.serializers.request.create import ReturnItemRequest
from biller_apps.return_item.dataclasses.request.delete import ReturnItemDelete
from biller_apps.return_item.serializers.request.update import ReturnItemUpdate
from biller_apps.return_item.serializers.request.get import ReturnItemGet
from biller_apps.return_item.views import ReturnItemView
from biller_apps.billing.models.billing import Billing
from biller_apps.return_item.models import ReturnItem
from biller_apps.supplier.models import Supplier
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.test_setup import TestSetUp
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
        return_id = ReturnItem().create(
                bill_id= self.bill_id, 
                supplier_id= 1, 
                organisation_id= 1, 
                item_id= self.item_id[0],
                organisation_name= "test", 
                return_reason= "test", 
                quantity= 10.0, 
                price= 200.0, 
                tax= 10.0
            )
        return_code = ReturnItem.objects.filter(return_id=return_id).first().return_code
        obj = ReturnItemGet(return_code=return_code,values='')
        resp = ReturnItemView().get_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        bill = self.bill_id
        bill_number = Billing.objects.filter(billing_id = bill).first().bill_number
        item_code=Items.objects.filter(item_id=self.item_id[0]).first().item_code
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        obj = ReturnItemRequest(purchase_bill_number=bill_number,supplier_code=supplier_code,item_code=item_code,return_reason="test",
                                quantity=10.0,price=10.0,tax=10.0)
        resp = ReturnItemView().create_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        return_id = ReturnItem().create(
                bill_id= self.bill_id, 
                supplier_id= 1, 
                organisation_id= 1, 
                item_id= self.item_id[0],
                organisation_name= "test", 
                return_reason= "test", 
                quantity= 10.0, 
                price= 200.0, 
                tax= 10.0
            )
        bill_number = Billing.objects.filter(billing_id = self.bill_id).first().bill_number
        return_code = ReturnItem.objects.filter(return_id=return_id).first().return_code
        obj = ReturnItemUpdate(purchase_bill_number=bill_number,return_code=return_code,supplier_code=1,item_code=1,return_reason="test",
                                quantity=10.0,price=200.0,tax=10.0)
        resp = ReturnItemView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        return_id = ReturnItem().create(
                bill_id= self.bill_id, 
                supplier_id= 1, 
                organisation_id= 1, 
                item_id= self.item_id[0],
                organisation_name= "test", 
                return_reason= "test", 
                quantity= 10.0, 
                price= 200.0, 
                tax= 10.0
            )
        return_code = ReturnItem.objects.filter(return_id=return_id).first().return_code
        print(return_code)
        obj = ReturnItemDelete(return_code=return_code)
        resp = ReturnItemView().delete_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
    
    def test_get_item_by_bill_extract(self):
        item = Items().create(name="new_tem", description= "it is good", created_time= datetime.datetime(2020, 1, 1).date(), bar_qr_auto= True, organisation_name= "new_org",
                                    bar_qr_code= "test", organisation_id= 1, brand_id=1, category_id= 1, supplier_id= 1,
                                    image_url= "http://example.com/img")
        bill= Billing().create(created_at=datetime.datetime(2020, 1, 1).date(), employee_id= 1, item_id=item[0], organisation_id=1,
                                        shop_id=self.shop_id, quantity=10.0, mrp_price=10.0)
        bill_number = Billing.objects.filter(billing_id=bill).first().bill_number
        obj = ReturnItemGetByBill(bill_number=bill_number,values='')
        resp = ReturnItemView().get_item_by_bill_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
