from biller_apps.return_item.models import ReturnItem
from biller_apps.test_setup import TestSetUp
from biller_apps.billing.models.billing import Billing

import datetime

class TestItemModels(TestSetUp):

    def test_create(self):
        res = ReturnItem().create(
                bill_id= self.bill_id, 
                supplier_id= self.supplier_id, 
                organisation_id= self.organisation_id, 
                item_id= self.item_id[0],
                organisation_name= "test", 
                return_reason= "test", 
                quantity= 10.0, 
                price= 200.0, 
                tax= 10.0
            )
        assert isinstance(res, int)

    def test_get_all(self):
        resp = ReturnItem().get_all(organisation_name='test')
        assert len(resp) > 0

    def test_update(self):
        resp = ReturnItem().update(return_id= self.return_item_id, 
                                   return_reason= "test", 
                                   quantity= 10.0, 
                                   price= 200.0, 
                                   tax= 10.0)
        assert isinstance(resp, int)

    def test_remove(self):
        data_id = ReturnItem().create(
                bill_id= self.bill_id, 
                supplier_id= self.supplier_id, 
                organisation_id= self.organisation_id, 
                item_id= self.item_id[0],
                organisation_name= "test", 
                return_reason= "test", 
                quantity= 10.0, 
                price= 200.0, 
                tax= 10.0
            )
        resp = ReturnItem().remove(return_id=data_id)
        assert resp == None

    def test_get(self):
        data_id = ReturnItem().create(
                bill_id= self.bill_id, 
                supplier_id= self.supplier_id, 
                organisation_id= self.organisation_id, 
                item_id= self.item_id[0],
                organisation_name= "test", 
                return_reason= "test", 
                quantity= 10.0, 
                price= 200.0, 
                tax= 10.0
            )
        return_code = ReturnItem.objects.filter(return_id = data_id).first().return_code
        resp = ReturnItem().get(return_code=return_code,organisation_name='test')
        assert len(resp) >= 0
    
    def test_get_item_by_bill(self):
        bill = self.bill_id
        bill_number = Billing.objects.filter(billing_id = bill).first().bill_number
        resp = ReturnItem().get_item_by_bill(bill_number=bill_number, organisation_name="test")
        assert len(resp) >= 0
    
    def test_calculate_total_price(self):
        resp = ReturnItem().calculate_total_price(quantity=10.0,tax=10.0,price=200.0)
        assert isinstance(resp, float)


        
