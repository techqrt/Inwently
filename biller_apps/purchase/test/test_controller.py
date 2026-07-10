import jwt
from django.urls import reverse
import datetime
from django.utils.timezone import make_aware
from biller.settings import SECRET_KEY
from biller_apps.test_setup import TestSetUp
from biller_apps.item.models.items import Items
from biller_apps.billing.models.billing import Billing
from biller_apps.purchase.models import Purchase
from biller_apps.supplier.models import Supplier


class TestController(TestSetUp):
    def test_create(self):
        item_id = self.item_id[0]
        bill_id = Billing(billing_id = 2).create(created_at=datetime.datetime(2020, 1, 1).date(), employee_id=1, item_id=item_id, organisation_id=1,
                                        shop_id=self.shop_id, quantity=10.0, mrp_price=10.0)
        item_code=Items.objects.filter(item_id=item_id).first().item_code
        bill_number = Billing.objects.filter(billing_id = bill_id[0]).first().bill_number
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        payload = {"data": [
            {
                "purchase_bill_number":bill_number,
                "supplier_code": supplier_code,
                "item_code": item_code,
                "buying_price":100.0,
                "landing_cost": 100.0,
                "selling_price": 100.0,
                "tax": 10.0,
                "quantity": 10.0,
                "bill_amount": 100.0
            }
        ]
    }
        res = self.client.post(reverse('purchase_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)
    
    def test_get_all(self):
        res = self.client.get(reverse('purchase_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get(self):
        purchase_id =  Purchase(purchase_id=2).create(
            purchase_bill_number="00001",
            supplier_id=self.supplier_id,
            item_id=self.item_id[0],
            buying_price=100.0,
            organisation_id=self.organisation_id,
            organisation_name='Test Organisation',
            landing_cost=110.0,
            selling_price=150.0,
            tax=10.0,
            quantity=5.0,
            bill_amount=550.0
        )

        purchase_code = Purchase.objects.filter(purchase_id=purchase_id).first().purchase_code
        res = self.client.get(reverse('purchase_get')+ f"?purchase_code={purchase_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)
        
    def test_delete(self):
        purchase_id =  Purchase(purchase_id=2).create(
            purchase_bill_number="00001",
            supplier_id=self.supplier_id,
            item_id=self.item_id[0],
            buying_price=100.0,
            organisation_id=self.organisation_id,
            organisation_name='Test Organisation',
            landing_cost=110.0,
            selling_price=150.0,
            tax=10.0,
            quantity=5.0,
            bill_amount=550.0
        )
        purchase_code = Purchase.objects.filter(purchase_id=purchase_id).first().purchase_code
        res = self.client.delete(reverse('purchase_delete') + f"?purchase_code={purchase_code}",headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        created_at = make_aware(datetime.datetime(2020, 1, 1))
        item_id = self.item_id[0]
        purchase_id = self.purchase_id
        bill_id = Billing(billing_id = 2).create(created_at=created_at, employee_id=1, item_id=item_id, organisation_id=1,
                                        shop_id=self.shop_id, quantity=10.0, mrp_price=10.0)
        item_code=Items.objects.filter(item_id=item_id).first().item_code
        bill_number = Billing.objects.filter(billing_id = bill_id[0]).first().bill_number
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        purchase_code = Purchase.objects.filter(purchase_id=purchase_id).first().purchase_code
        payload = {
                "purchase_bill_number":bill_number,
                "supplier_code": supplier_code,
                "item_code": item_code,
                "buying_price":100.0,
                "landing_cost": 100.0,
                "selling_price": 100.0,
                "tax": 10.0,
                "quantity": 10.0,
                "bill_amount": 100.0,
                "purchase_code":purchase_code
            }
        res = self.client.put(reverse('purchase_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)
    
