import jwt
from django.urls import reverse
import datetime
from biller.settings import SECRET_KEY
from biller_apps.employees.views import EmployeesView
from biller_apps.test_setup import TestSetUp
from biller_apps.brand.models import Brand
from biller_apps.return_item.models import ReturnItem
from biller_apps.organisation.models import Organisation
from biller_apps.employees.models.employees import Employees
from biller_apps.category.models import Category
from biller_apps.item.models.items import Items
from biller_apps.supplier.models import Supplier
from biller_apps.billing.models.billing import Billing



class TestController(TestSetUp):
    def test_get(self):
        return_id = ReturnItem().create(
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
        return_code = ReturnItem.objects.filter(return_id=return_id).first().return_code
        res = self.client.get(reverse('return_item_get')+ f"?return_code={return_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)
        
    def test_delete(self):
        return_id = ReturnItem().create(
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
        return_code = ReturnItem.objects.filter(return_id=return_id).first().return_code
        res = self.client.delete(reverse('return_item_delete') + f"?return_code={return_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        bill = self.bill_id
        supplier = self.supplier_id
        item = self.item_id
        return_id = self.return_item_id
        return_code = ReturnItem.objects.filter(return_id=return_id).first().return_code
        item_code = Items.objects.filter(item_id = item[0]).first().item_code
        supplier_code = Supplier.objects.filter(supplier_id=supplier).first().supplier_code
        bill_number = Billing.objects.filter(billing_id = bill).first().bill_number
        payload = {
                "purchase_bill_number":bill_number,
                "supplier_code":supplier_code,
                "item_code":item_code,
                "return_code": return_code,
                "return_reason": "test", 
                "quantity": 10.0, 
                "price": 200.0, 
                "tax": 10.0
            }
        res = self.client.put(reverse('return_item_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        bill = self.bill_id
        supplier = self.supplier_id
        item = self.item_id
        item_code = Items.objects.filter(item_id = item[0]).first().item_code
        supplier_code = Supplier.objects.filter(supplier_id=supplier).first().supplier_code
        bill_number = Billing.objects.filter(billing_id = bill).first().bill_number
        payload = {
                "purchase_bill_number":bill_number,
                "supplier_code":supplier_code,
                "item_code":item_code,
                "return_reason": "test", 
                "quantity": 10.0, 
                "price": 200.0, 
                "tax": 10.0
            }
        res = self.client.post(reverse('return_item_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)
    
    def test_get_by_bill(self):
        bill = self.bill_id
        bill_number = Billing.objects.filter(billing_id = bill).first().bill_number
        res = self.client.get(reverse('return_item_get_by_bill')+ f"?bill_number={bill_number}", format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    def test_get_all(self):
        res = self.client.get(reverse('return_item_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)