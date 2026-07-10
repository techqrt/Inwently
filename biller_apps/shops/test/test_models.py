from biller_apps.shops.models import Shops
from biller_apps.test_setup import TestSetUp
from biller_apps.organisation.models import Organisation
import datetime

class TestItemModels(TestSetUp):

    def test_create(self):
        data = Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-')
        res = data
        assert isinstance(res, int)

    def test_get_all(self):
        resp = Shops().get_all(organisation_name="test", type="CUSTOM")
        assert len(resp) > 0

    def test_update(self):
        data = Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-'
                )
        shop_id = data

        resp = Shops().update(name="test1", shop_id=shop_id, email_id="test@gmail.com", 
                              mobile_number="435435345435",alt_mobile_number="-", 
                              website="www.example.com", type= "CUSTOM")
        assert isinstance(resp, int)

    def test_remove(self):
        data = Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-'
                )
        shop_id = data
        resp = Shops().remove(shop_id=shop_id)
        assert resp == None

    def test_get(self):
        Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-'
                )
        resp = Shops().get(name="test1", organisation_id= 1, single=True)
        assert isinstance(resp, dict)
    
    def test_get_by_code(self):
        shop=Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-'
                )
        shop_code = Shops.objects.filter(shop_id=shop).first().shop_code
        resp = Shops().get_by_code(shop_code= shop_code)
        assert isinstance(list(resp), list)
    
    def test_remove_from_list(item_ids: list):
        shop=Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-'
                )
        resp = Shops().remove_from_list(shop_id=[shop])
        assert resp == None
    
    def test_get_by_name_list(self):
        shop=Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-'
                )
        shop_name = Shops.objects.filter(shop_id=shop).first().name
        resp = Shops().get_by_name_list(name= shop_name)
        assert isinstance(list(resp), list)

    def test_get_by_ids(self):
        shop=Shops().create(
                name="test1", organisation_name="test", organisation_id=1,
                address_id=1, website='-', email_id='-', mobile_number='-',
                alt_mobile_number='0', type='-'
                )
        resp = Shops().get_by_ids(shop_ids=[shop])
        assert isinstance(list(resp),list)


        
