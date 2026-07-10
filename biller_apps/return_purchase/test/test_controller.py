import jwt
from django.urls import reverse
import datetime
from biller.settings import SECRET_KEY
from biller_apps.employees.views import EmployeesView
from biller_apps.test_setup import TestSetUp
from biller_apps.brand.models import Brand
from biller_apps.return_purchase.models import ReturnPurchase
from biller_apps.organisation.models import Organisation
from biller_apps.employees.models.employees import Employees
from biller_apps.category.models import Category
from biller_apps.item.models.items import Items
from biller_apps.supplier.models import Supplier
from biller_apps.billing.models.billing import Billing
from biller_apps.purchase.models import Purchase




class TestController(TestSetUp):
    def test_get(self):
        purchase_id = self.purchase_id
        item_id = self.item_id[0]
        return_id = ReturnPurchase().create(purchase_id=purchase_id, 
                                            supplier_id=self.supplier_id, 
                                            organisation_id=self.organisation_id, 
                                            item_id= item_id,
                                            organisation_name= "test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        return_code = ReturnPurchase.objects.filter(return_id=return_id).first().return_code
        res = self.client.get(reverse('return_purchase_get') + f"?return_code={return_code}", headers=self.header)
        print(res.json())
        self.assertEqual(res.status_code, 200)
    
    def test_delete(self):
        return_id = ReturnPurchase().create(purchase_id=self.purchase_id, 
                                            supplier_id= self.supplier_id, 
                                            organisation_id= self.organisation_id, 
                                            item_id= self.item_id[0],
                                            organisation_name= "test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        return_code = ReturnPurchase.objects.filter(return_id=return_id).first().return_code
        res = self.client.delete(reverse('return_purchase_delete') + f"?return_code={return_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        return_id = ReturnPurchase().create(purchase_id=self.purchase_id, 
                                            supplier_id= self.supplier_id, 
                                            organisation_id= self.organisation_id, 
                                            item_id= self.item_id[0],
                                            organisation_name= "test", 
                                            return_reason="test", 
                                            quantity= 10.0, 
                                            tax= 10.0, 
                                            total_price=10.0
            )
        return_code = ReturnPurchase.objects.filter(return_id=return_id).first().return_code
        payload = {"purchase_id": self.purchase_id,
                        "supplier_id": self.supplier_id,
                        "organisation_id": self.organisation_id,
                        "item_id": self.item_id[0],
                        "return_reason": "test",
                        "quantity":10.0,
                        "return_code":return_code,
                        "tax":10.0,
                        "total_price":10.0
                    }
        res = self.client.put(reverse('return_purchase_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        payload = {
                    "data": [
                                {
                                "purchase_id": self.purchase_id,
                                "supplier_id": self.supplier_id,
                                "organisation_id": self.organisation_id,
                                "item_id": self.item_id[0],
                                "return_reason": "test",
                                "quantity":10.0,
                                "tax":10.0,
                                "total_price":10.0
                                }
                            ]
                        }
        res = self.client.post(reverse('return_purchase_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)
    
    def test_get_by_bill(self):
        bill = self.bill_id
        bill_number = Billing.objects.filter(billing_id = bill).first().bill_number
        res = self.client.get(reverse('return_item_get_by_bill')+ f"?bill_number={bill_number}", format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    def test_get_all(self):
        res = self.client.get(reverse('return_purchase_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)