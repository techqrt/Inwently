from biller_apps.purchase.models import Purchase
from biller_apps.billing.models.billing import Billing
from biller_apps.test_setup import TestSetUp
import datetime

class TestPurchaseModels(TestSetUp):

    def test_create(self):
        resp = Purchase(purchase_id = 15).create(
            purchase_bill_number=self.bill_number,
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
        assert isinstance(resp, int)

    def test_get_all(self):
        resp = Purchase.get_all(organisation_name='test')
        assert len(resp) > 0

    def test_get(self):
        purchase_id = Purchase(purchase_id=20).create(
            purchase_bill_number=self.bill_number,
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
        resp = Purchase.get(purchase_code=purchase_code,organisation_name='test')
        assert isinstance(resp, dict)

    def test_update(self):
        resp = Purchase.update(
            purchase_id=self.purchase_id,
            buying_price=120.0,
            landing_cost=130.0,
            selling_price=160.0,
            tax=15.0,
            quantity=10.0,
            bill_amount=1750.0
        )
        assert isinstance(resp, int)

    def test_remove(self):
        resp = Purchase.remove(purchase_id=self.purchase_id)
        assert resp is None
