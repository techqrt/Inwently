from django.urls import reverse
import json

from biller_apps.test_setup import TestSetUp
from biller_apps.taxes.models import Taxes
from rest_framework import status


class TestTaxesViewController(TestSetUp):

    def test_create(self):
        payload = {"name": "new_tax", "total_tax": 18.0, "tax_splits": {"cgst": 9.0, "sgst": 9.0}}
        res = self.client.post(reverse('taxes_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)
    
    def test_get_all(self):
        res = self.client.get(reverse('taxes_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    def test_update(self):
        tax = Taxes()
        tax_id = tax.create(name="Old Tax", total_tax=5.0, tax_splits={"cgst": 2.5, "sgst": 2.5}, organisation_id=self.organisation_id, organisation_name="TestOrg")

        tax_obj = Taxes.objects.get(tax_id=tax_id)
        payload = {
            "tax_code": tax_obj.tax_code,
            "name": "Updated Tax",
            "total_tax": 10.0,
            "tax_splits": {"cgst": 5.0, "sgst": 5.0}
        }
        resp = self.client.put(reverse('taxes_update'), data=payload, format="json", headers=self.header)
        self.assertEqual(resp.status_code, 201)
    
    def test_search(self):
        res = self.client.get(reverse('taxes_search') + '?key={tax.name}', headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_many(self):
        tax1 = Taxes()
        tax1_id = tax1.create(name="Tax1", total_tax=5.0, tax_splits={"cgst": 2.5, "sgst": 2.5}, organisation_id=self.organisation_id, organisation_name="TestOrg")
        
        tax2 = Taxes()
        tax2_id = tax2.create(name="Tax2", total_tax=12.0, tax_splits={"cgst": 6.0, "sgst": 6.0}, organisation_id=self.organisation_id, organisation_name="TestOrg")
        
        tax1_obj = Taxes.objects.get(tax_id=tax1_id)
        tax2_obj = Taxes.objects.get(tax_id=tax2_id)
        payload = {
            "tax_codes": [tax1_obj.tax_code, tax2_obj.tax_code]
        }
        res = self.client.patch(reverse('taxes_delete_many'), data=payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)
