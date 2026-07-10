import jwt
from django.urls import reverse
import datetime
from biller.settings import SECRET_KEY
from biller_apps.employees.views import EmployeesView
from biller_apps.test_setup import TestSetUp
from biller_apps.brand.models import Brand
from biller_apps.shops.models import Shops
from biller_apps.organisation.models import Organisation
from biller_apps.employees.models.employees import Employees
from biller_apps.category.models import Category
from biller_apps.item.models.items import Items
from biller_apps.supplier.models import Supplier


class TestController(TestSetUp):
    def test_get_all(self):
        res = self.client.get(reverse('shop_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get(self):
        data = Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-')
        shop_code = Shops.objects.filter(shop_id=data).first().shop_code
        res = self.client.get(reverse('shop_get')+ f"?shop_code={shop_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)
        
    def test_delete(self):
        shop = Shops.objects.filter(shop_id=self.shop_id).first()

    # Check if Organisation uses this address before unsetting
        Employees.objects.filter(address_id=shop.address_id).update(address_id=1)
        Organisation.objects.filter(address_id=shop.address_id).update(address_id=1)  # Assign a valid default address ID

        res = self.client.delete(reverse('shop_delete') + f"?shop_code={shop.shop_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        shop_code = Shops.objects.filter(shop_id=self.shop_id).first().shop_code
        payload = {
            "name":"test2",
            "state": "delhi",
            "country":"india",
            "street":"daravi",
            "type":"CUSTOM",
            "email_id":"test34@gmail.com",
            "mobile_number":"1233334556",
            "shop_code":shop_code,
            "alt_mobile_number":"4433223423423",
            "website":"www.example.com"
            }
        res = self.client.put(reverse('shop_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        Shops.objects.all().delete()
        payload = {
            "name":"alfat",
            "state": "delhi",
            "country":"india",
            "street":"daravi",
            "type":"CUSTOM",
            "email_id":"test34@gmail.com",
            "mobile_number":"1233334556",
            "alt_mobile_number":"4433223423423",
            "website":"www.example.com"
            }
        res = self.client.post(reverse('shop_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)

    def test_delete_many(self):
        shop = Shops.objects.filter(shop_id=self.shop_id).first()

        # Ensure employees using this shop's address have a valid address before deletion
        Employees.objects.filter(address_id=shop.address_id).update(address_id=1)
        Organisation.objects.filter(address_id=shop.address_id).update(address_id=1)  # Assign a valid default address ID

        # Ensure shop_code is a list (if multiple shops need deletion)
        shop_codes = [shop.shop_code] if isinstance(shop.shop_code, str) else shop.shop_code

        query_string = "&".join([f"shop_code={code}" for code in shop_codes])  
        url = f"{reverse('shop_delete')}?{query_string}"  # Pass as query params
        
        res = self.client.delete(url, headers=self.header)  # Remove body
        self.assertEqual(res.status_code, 200)
    
    def test_search(self):
        res = self.client.get(reverse('shop_search') + '?key=test', headers=self.header)
        self.assertEqual(res.status_code, 200)
