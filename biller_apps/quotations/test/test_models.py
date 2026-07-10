from biller_apps.quotations.models import Quotation
from biller_apps.test_setup import TestSetUp
from biller_apps.common.dataclasses.get_all import GetAll


class TestQuotationModels(TestSetUp):

    def test_create(self):
        resp = Quotation().create(
            supplier_id=self.supplier_id,
            organisation_id=self.organisation_id,
            organisation_name='Test Organisation',
            item_id=self.item_id[0],
            description='Test Description',
            brand='Test Brand',
            quantity=10.0,
            price=200.0,
            tax=20.0,
            purchase=True,
            sales=False
        )
        assert isinstance(resp, int)

    def test_get_all(self):
        params = GetAll(page_num=1,limit=1,sort_by='quotation_code',sort_order='asc',values='',filter_key='purchase',filter_value=True,search_key='name') 
        resp = Quotation.get_all(organisation_name='Test Organisation',params=params)
        assert isinstance(list(resp), list)

    def test_get(self):
        quo_id = Quotation().create(
            supplier_id=self.supplier_id,
            organisation_id=self.organisation_id,
            organisation_name='Test',
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
        resp = Quotation().get(quotation_code=quo_code,organisation_name='test')
        assert isinstance(resp, dict)

    def test_update(self):
        resp = Quotation.update(
            quotation_id=self.quotation_id,
            description='Updated Description',
            brand='Updated Brand',
            quantity=15.0,
            price=250.0,
            tax=25.0,
            purchase=False,
            sales=True
        )
        assert isinstance(resp, int)

    def test_remove(self):
        resp = Quotation.remove(quotation_id=self.quotation_id)
        assert resp is None
    def test_calculate_total_price(self):
        resp = Quotation.calculate_total_price(price=100.1,tax=2.1,quantity=10.1)
        assert isinstance(resp, float)
