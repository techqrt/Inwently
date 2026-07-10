from django.urls import reverse
from rest_framework.test import APITestCase
import datetime

from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.return_item.dataclasses.request.get_by_bill import ReturnItemGetByBill
from biller_apps.return_purchase.serializers.request.create import ReturnPurchaseRequest
from biller_apps.return_purchase.dataclasses.request.delete import ReturnPurchaseDelete
from biller_apps.return_purchase.serializers.request.update import ReturnPurchaseUpdate
from biller_apps.return_purchase.serializers.request.get import ReturnPurchaseGet
from biller_apps.return_purchase.views import ReturnPurchaseView
from biller_apps.billing.models.billing import Billing
from biller_apps.return_purchase.models import ReturnPurchase
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
        purchase_id = self.purchase_id
        item_id = self.item_id[0]
        return_id = ReturnPurchase().create(purchase_id=purchase_id, 
                                            supplier_id= 1, 
                                            organisation_id= 1, 
                                            item_id= item_id,
                                            organisation_name= "test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        
        return_code = ReturnPurchase.objects.filter(return_id=return_id).first().return_code
        obj = ReturnPurchaseGet(return_code=return_code,values='')
        resp = ReturnPurchaseView().get_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
         purchase_id = self.purchase_id
         item_id = self.item_id[0]
         obj = ReturnPurchaseRequest(purchase_id=purchase_id,supplier_id= 1,organisation_id= 1, 
                                    item_id= item_id,return_reason="test", 
                                    quantity= 10.0,tax= 10.0,total_price=10.0)
         resp = ReturnPurchaseView().create_extract(params=[obj],token_payload=self.token_payload)
         self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        purchase_id = self.purchase_id
        item_id = self.item_id[0]
        return_id = ReturnPurchase().create(purchase_id=purchase_id, 
                                            supplier_id= 1, 
                                            organisation_id= 1, 
                                            item_id= item_id,
                                            organisation_name= "test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        return_code = ReturnPurchase.objects.filter(return_id=return_id).first().return_code
        obj = ReturnPurchaseUpdate(purchase_id=purchase_id,supplier_id= 1,organisation_id= 1, 
                                    item_id= item_id,return_reason="test",return_code=return_code, 
                                    quantity= 10.0,tax= 10.0,total_price=10.0)
        resp = ReturnPurchaseView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        purchase_id = self.purchase_id
        item_id = self.item_id[0]
        return_id = ReturnPurchase().create(purchase_id=purchase_id, 
                                            supplier_id= 1, 
                                            organisation_id= 1, 
                                            item_id= item_id,
                                            organisation_name= "test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        return_code = ReturnPurchase.objects.filter(return_id=return_id).first().return_code
        obj = ReturnPurchaseDelete(return_code=return_code)
        resp = ReturnPurchaseView().delete_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
    
    def test_get_all_extract(self):
        obj = GetAll(limit=2, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='')
        resp = ReturnPurchaseView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
