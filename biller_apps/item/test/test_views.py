from django.urls import reverse
from rest_framework.test import APITestCase
import datetime

from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.item.dataclasses.request.delete_many import ItemDeleteManyRequest
from biller_apps.item.serializers.request.create import ItemRequest
from biller_apps.item.dataclasses.request.delete import ItemDelete
from biller_apps.item.serializers.request.update import ItemUpdate
from biller_apps.item.serializers.request.get import ItemGet
from biller_apps.item.views import ItemView
from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.supplier.models import Supplier
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.test_setup import TestSetUp
from biller_apps.item.models.items import Items



class TestViews(TestSetUp, APITestCase):
    
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
    

    def test_get_extract(self):
        item_id = Items().create(
                name="hqwel",
                description="test description",
                created_time=datetime.datetime.now(tz=datetime.timezone.utc),
                bar_qr_auto=True,
                organisation_id=1,
                brand_id=1,
                category_id=1,
                organisation_name= "test",
                bar_qr_code= "test",
                supplier_id=1,
                image_url="http://example.com/img"
            )
        item_id = item_id[0]
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        obj = ItemGet(item_code=item_code,values='')
        resp = ItemView().get_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='',search_key='')
        resp = ItemView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        brand_code=Brand.objects.filter(brand_id=self.brand_id).first().brand_code
        category_code=Category.objects.filter(category_id=self.category_id).first().category_code
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code
        obj = ItemRequest(name= "ezprints",description= "this is good",bar_qr_code= "test",bar_qr_auto=True,brand_code=brand_code, 
                        category_code=category_code,supplier_code= supplier_code,created_time=datetime.datetime.now(tz=datetime.timezone.utc),image_url="http://example.com/img")
        resp = ItemView().create_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_update_extract(self):
        item_id = Items().create(
                name="hqwel",
                description="test description",
                created_time=datetime.datetime.now(tz=datetime.timezone.utc),
                bar_qr_auto=True,
                organisation_id=1,
                brand_id=1,
                category_id=1,
                organisation_name= "test",
                bar_qr_code= "test",
                supplier_id=1,
                image_url="http://example.com/img"
            )
        item_id = item_id[0]
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        brand_code=Brand.objects.filter(brand_id=self.brand_id).first().brand_code
        category_code=Category.objects.filter(category_id=self.category_id).first().category_code
        supplier_code = Supplier.objects.filter(supplier_id=self.supplier_id).first().supplier_code 
        obj = ItemUpdate(
            name="newhawel",
            item_code=item_code,
            description="this is an updated product",
            bar_qr_code="updated_test",
            brand_code=brand_code,
            category_code=category_code,
            supplier_code=supplier_code,
            created_time="2025-04-12T15:07:51.384Z",
            image_url="http://example.com/img"
        )

        resp = ItemView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        item_id = Items().create(
                name="hqwel",
                description="test description",
                created_time=datetime.datetime.now(tz=datetime.timezone.utc),
                bar_qr_auto=True,
                organisation_id=1,
                brand_id=1,
                category_id=1,
                organisation_name= "test",
                bar_qr_code= "test",
                supplier_id=1,
                image_url="http://example.com/img"
            )
        item_id = item_id[0]
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        obj = ItemDelete(item_code=item_code)
        resp = ItemView().delete_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
    
    def test_delete_many_extract(self):
        item_id = Items().create(
                name="hqwel",
                description="test description",
                created_time=datetime.datetime.now(tz=datetime.timezone.utc),
                bar_qr_auto=True,
                organisation_id=1,
                brand_id=1,
                category_id=1,
                organisation_name= "test",
                bar_qr_code= "test",
                supplier_id=1,
                image_url="http://example.com/img"
            )
        item_id = item_id[0]
        item_code = Items.objects.filter(item_id=item_id).first().item_code
        obj = ItemDeleteManyRequest(item_code=[item_code])
        resp = ItemView().delete_many_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
