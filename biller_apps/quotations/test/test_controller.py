import jwt
from django.urls import reverse
import datetime
from biller.settings import SECRET_KEY
from biller_apps.employees.views import EmployeesView
from biller_apps.test_setup import TestSetUp
from biller_apps.brand.models import Brand
from biller_apps.quotations.models import Quotation
from biller_apps.organisation.models import Organisation
from biller_apps.employees.models.employees import Employees
from biller_apps.category.models import Category
from biller_apps.item.models.items import Items
from biller_apps.supplier.models import Supplier


class TestController(TestSetUp):
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
        quo_code = Quotation.objects.filter(quotation_id=quo_id).first().quotation_code
        res = self.client.get(reverse('quotation_get')+ f"?quotation_code={quo_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)
        
    def test_delete(self):
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
        quo_code = Quotation.objects.filter(quotation_id=quo_id).first().quotation_code 

        res = self.client.delete(reverse('quotation_delete') + f"?quotation_code={quo_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        quo_code = Quotation.objects.filter(quotation_id=self.quotation_id).first().quotation_code
        payload = {
                "supplier_id": self.supplier_id,
                "organisation_id": self.organisation_id,
                "organisation_name": 'test',
                "item_id": self.item_id[0],
                "description": 'test',
                "quotation_code":quo_code,
                "brand": 'test',
                "quantity": 10.0,
                "price": 200.0,
                "tax": 20.0,
                "total":10.0,
                "purchase": True,
                "sales": False
            }
        res = self.client.put(reverse('quotation_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        payload = {
        "data": [ 
            {
                "supplier_id": self.supplier_id,
                "organisation_id": self.organisation_id,
                "organisation_name": 'Test',
                "item_id": self.item_id[0],
                "description": 'Test Description',
                "brand": 'Test Brand',
                "quantity": 10.0,
                "price": 200.0,
                "tax": 20.0,
                "total":10.0,
                "purchase": True,
                "sales": False
            }
        ]
    }
        res = self.client.post(reverse('quotation_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)

    def test_get_all(self):
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
        response = self.client.get(reverse('quotation_get_all')+ f"?filter_key=purchase&filter_value=True&limit=20&page_num=1&sort_by=quotation_code&sort_order=asc", 
            headers=self.header)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        
    def test_search(self):
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
        quo_code = Quotation.objects.filter(quotation_id=quo_id).first().quotation_code 
        resp = self.client.get(reverse('quotation_search')+f"?key=quo_code",headers=self.header)
        self.assertEqual(resp.status_code,200)
        