from biller_apps.return_purchase.models import ReturnPurchase
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.test_setup import TestSetUp
import datetime

class TestItemModels(TestSetUp):
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

    def test_create(self):
        purchase_id = self.purchase_id
        item_id = self.item_id[0]
        res = ReturnPurchase().create(purchase_id=purchase_id, 
                                            supplier_id= 1, 
                                            organisation_id= 1, 
                                            item_id= item_id,
                                            organisation_name= "test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        assert isinstance(res, int)

    def test_update(self):
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
        resp = ReturnPurchase().update(return_id= return_id, 
                                       return_reason="test", 
                                       quantity= 10.1, 
                                       tax= 10.0, 
                                       total_price= 10.0)
        assert isinstance(resp, int)

    def test_remove(self):
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
        resp = ReturnPurchase().remove(return_id=return_id)
        assert resp == None

    def test_get(self):
        purchase_id = self.purchase_id
        item_id = self.item_id[0]
        return_id = ReturnPurchase().create(purchase_id=purchase_id, 
                                            supplier_id= 1, 
                                            organisation_id= 1, 
                                            item_id= item_id,
                                            organisation_name= "Test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        return_code = ReturnPurchase.objects.filter(return_id=return_id).first().return_code
        resp = ReturnPurchase().get(return_code=return_code,organisation_name=self.token_payload.organisationName)
        assert isinstance(resp, dict)
    
    def test_calculate_total_price(self):
        resp = ReturnPurchase().calculate_total_price(quantity=10.0,tax=10.0)
        assert isinstance(resp, float)

    


        
