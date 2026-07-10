from biller_apps.taxes.models import Taxes
from django.db.utils import IntegrityError
from biller_apps.test_setup import TestSetUp

class TestTaxesModels(TestSetUp):
    def test_create(self):
        resp = Taxes().create(name='test', total_tax=10.5, tax_splits={'cgst': 5.0, 'sgst': 5.5}, organisation_id=self.organisation_id, organisation_name='test', secure=False)
        assert isinstance(resp, int)
    
    def test_create_secure_tax(self):   
        resp = Taxes().create(name='test', total_tax=10.5, tax_splits={'cgst': 5.0, 'sgst': 5.5}, organisation_id=self.organisation_id, organisation_name='test', secure=True)
        assert isinstance(resp, int)

    def test_get_all(self):
        resp = Taxes.get_all(organisation_name='test')
        assert len(resp) >= 0

    def test_update(self):
        tax_id = Taxes().create(name='test', total_tax=10.5, tax_splits={'cgst': 5.0, 'sgst': 5.5}, organisation_id=self.organisation_id, organisation_name='test')
        updated_tax_id = Taxes.update(tax_id=tax_id, name='Updated Test', total_tax=12.0, tax_splits={'cgst': 6.0, 'sgst': 6.0})
        assert updated_tax_id == tax_id
    
    def test_get(self):
        tax_id = Taxes().create(name='test', total_tax=10.5, tax_splits={'cgst': 5.0, 'sgst': 5.5}, organisation_id=self.organisation_id, organisation_name='test')
        tax = Taxes.get(organisation_name='test', tax_code=Taxes.objects.get(tax_id=tax_id).tax_code)
        assert tax is not None

    def test_get_from_list(self):
        resp = Taxes.get_from_list(organisation_name='test', tax_codes=['T_1', 'T_2'])
        assert len(resp) >= 0

    def test_delete_many(self):
        tax1 = Taxes().create(name='test1', total_tax=5.0, tax_splits={'cgst': 2.5, 'sgst': 2.5}, organisation_id=self.organisation_id, organisation_name='test')
        tax2 = Taxes().create(name='test2', total_tax=7.0, tax_splits={'cgst': 3.5, 'sgst': 3.5}, organisation_id=self.organisation_id, organisation_name='test')
        Taxes.delete_many(organisation_name='test', tax_codes=[Taxes.objects.get(tax_id=tax1).tax_code, Taxes.objects.get(tax_id=tax2).tax_code])
        assert Taxes.objects.filter(tax_id__in=[tax1, tax2]).count() == 0  

    def test_get_sorted_taxes_ascending(self):
        resp = Taxes.get_sorted_taxes(organisation_name='Test',sort_order= 'asc')
        assert resp is not None
    
    def test_get_sorted_taxes_descending(self):
        resp = Taxes.get_sorted_taxes("Test", "desc")
        assert resp is not None
