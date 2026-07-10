from django.urls import reverse
from rest_framework.test import APITestCase
import datetime

from biller_apps.auth.dataclasses.request.token import TokenPayload
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.shops.serializers.request.create import ShopsRequest
from biller_apps.shops.dataclases.request.delete import ShopsDelete
from biller_apps.common.dataclasses.search import Search
from biller_apps.shops.dataclases.request.delete_many import ShopsDeleteMany
from biller_apps.shops.serializers.request.update import ShopsUpdateRequest
from biller_apps.shops.serializers.request.get import ShopGet
from biller_apps.shops.views import ShopsView
from biller_apps.brand.models import Brand
from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation
from biller_apps.employees.models.employees import Employees
from biller_apps.shops.dataclases.request.get_all import ShopGetAll
from biller_apps.test_setup import TestSetUp
from biller_apps.shops.models import Shops



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
        shop_id = Shops().create(
                name="altaf", 
                organisation_name= "test5", 
                organisation_id=1, 
                address_id=1, 
                website= "www.example.com",
                email_id="test1@gmail.com", 
                mobile_number="121221212323", 
                alt_mobile_number="827483284329", 
                type= "CUSTOM"
            )
        shop_code = Shops.objects.filter(shop_id=shop_id).first().shop_code
        obj = ShopGet(shop_code=shop_code, values='')
        resp = ShopsView().get_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_extract(self):
        obj = ShopGetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='',type='')
        resp = ShopsView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        obj = ShopsRequest(name="test1",state="kerala",country="india",street="thrissur",
                           type= "CUSTOM",email_id= "testsha@gmail.com",mobile_number="23546454645",
                           alt_mobile_number="8745743548",website="www.new.com")
        resp = ShopsView().create_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        shop_id = Shops().create(name="test1", organisation_name="test", organisation_id=1,
                                 address_id=1, website='-', email_id='-', mobile_number='-',
                                 alt_mobile_number='0', type='-')
        shop_code = Shops.objects.filter(shop_id=shop_id).first().shop_code
        obj = ShopsUpdateRequest(name="test1",state="kerala",shop_code=shop_code,country="india",street="thrissur",
                            type= "CUSTOM",email_id= "testsha@gmail.com",mobile_number="23546454645",
                            alt_mobile_number="8745743548",website="www.new.com"
        )
        resp = ShopsView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        default_address = Address().create(state="kerala", street="kuruppam", country="India")
        shop_id = Shops().create(name="test1", organisation_name="test", organisation_id=1,
                                 address_id=default_address, website='-', email_id='-', mobile_number='-',
                                 alt_mobile_number='0', type='-')
        shop = Shops.objects.get(shop_id=shop_id)
        Organisation.objects.filter(address_id=shop.address_id).update(address_id=default_address)
        obj = ShopsDelete(shop_code=shop.shop_code)        
        resp = ShopsView().delete_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
    
    def test_delete_many_extract(self):
        default_address = Address().create(state="kerala", street="kuruppam", country="India")
        shop_id = Shops().create(name="test1", organisation_name="test", organisation_id=1,
                                 address_id=default_address, website='-', email_id='-', mobile_number='-',
                                 alt_mobile_number='0', type='-')
        shop = Shops.objects.get(shop_id=shop_id)
        obj = ShopsDeleteMany(shop_code=[shop.shop_code])
        resp = ShopsView().delete_many_extract(params=obj,token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
    
    def test_search_extract(self):
        obj = Search(key="test", page_num=1, limit=10)
        resp = ShopsView().search_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
