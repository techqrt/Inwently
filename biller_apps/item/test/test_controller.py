
from django.urls import reverse
import datetime


from biller_apps.auth.dataclasses.request.token_payload import Payload

from biller_apps.item.dataclasses.request.create import ItemRequest
from biller_apps.item.views import ItemView
from biller_apps.test_setup import TestSetUp
from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.item.models.items import Items
from biller_apps.supplier.models import Supplier


class TestController(TestSetUp):
    def setUp(self):
        super().setUp()
        token_data = {
            "email_id": "harisjosinpeter@gmail.com",
            "expiry": "2025-02-07T17:39:44.056579",
            "organisationName": "Techaso",
            "organisation_id": 1,
            "present_url": "",
            "access_token": "",
            "method": "",
            "path": "",
            "approval": False,
            "permissions": {
                "master": {
                    "item": True,
                    "shop": True,
                    "supplier": True,
                    "customer": True,
                    "create": True,
                    "employee": True
                },
                "inventory": {"inventory": True},
                "billing": {
                    "pos": True,
                    "return_item": True,
                    "bill_history": True
                },
                "reports": {
                    "general": True,
                    "overview": True,
                    "administration": True,
                    "day_book": True,
                    "gst": True
                },
                "printer_templates": {"printer_templates": True},
                "dashboard": {"dashboard": True},
                "stock": {
                    "purchase_list": True,
                    "return_purchase": True,
                    "stock": True
                },
                "quotations": {"quotations": True}
            }
        }
        self.token_payload = Payload(**token_data)
    def test_get_all(self):
        res = self.client.get(reverse('item_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get(self):
        item_id = self.item_id[0]
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        res = self.client.get(reverse('item_get')+ f"?item_code={item_code}", headers=self.header)
        self.assertEqual(res.status_code, 200)
        
    def test_delete(self):
        item_id = self.item_id[0]
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        res = self.client.delete(reverse('item_delete') + f"?item_code={item_code}",headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        item_id = self.item_id[0]
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        brand_code=Brand.objects.filter(brand_id=self.brand_id).first().brand_code
        category_code=Category.objects.filter(category_id=self.category_id).first().category_code
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        payload = {
            "name": "test",
            "item_code": item_code,
            "description": "this item is excellent",
            "bar_qr_code": "test2",
            "brand_code": brand_code,
            "category_code": category_code,
            "supplier_code": supplier_code,
            "created_time": "2025-02-12T15:07:51.384Z",
            "image_url": "http://example.com/img"
            }
        res = self.client.put(reverse('item_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        brand_code=Brand.objects.filter(brand_id=self.brand_id).first().brand_code
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        category_code=Category.objects.filter(category_id=self.category_id).first().category_code
        payload = {
            "name": "testcom1",
            "description": "test",
            "bar_qr_code": "test",
            "bar_qr_auto": True,
            "brand_code": brand_code,
            "category_code": category_code,
            "supplier_code": supplier_code,
            "created_time": "2025-02-12T13:28:36.842Z",
            "image_url": "http://example.com/img"
        }
        res = self.client.post(reverse('item_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_delete_many(self):
        brand_code = Brand.objects.filter(brand_id=self.brand_id).first().brand_code
        category_code = Category.objects.filter(category_id=self.category_id).first().category_code
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        obj = ItemRequest(name="ezprints1", description="this is good", bar_qr_code="test", bar_qr_auto=True,
                          brand_code=brand_code,
                          category_code=category_code, supplier_code=supplier_code,
                          created_time=datetime.datetime.now(tz=datetime.timezone.utc),
                          image_url="http://example.com/img")
        resp = ItemView().create_extract(params=obj, token_payload=self.token_payload)
        resp = resp.data
        item_codes = [resp['data']['itemCode']]
        payload = {
              "item_code": item_codes
            }
        res = self.client.patch(reverse('item_delete_many'),payload,format="json", headers=self.header)  # Remove body
        print("response ",res.json())
        self.assertEqual(res.status_code, 200)
    
    def test_search(self):
        res = self.client.get(reverse('item_search') + '?key=test', headers=self.header)
        self.assertEqual(res.status_code, 200)
