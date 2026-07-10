from biller_apps.item.models.items import Items
from biller_apps.test_setup import TestSetUp
import datetime

class TestItemModels(TestSetUp):

    def test_create(self):
        data = Items().create(
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
        res = data[0]
        assert isinstance(res, int)

    def test_get_all(self):
        resp = Items().get(organisation_name='test')
        assert len(resp) > 0

    def test_update(self):
        data = Items().create(
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
        item_id = data[0]

        resp = Items().update(name="hqwel",
                description="test description",
                created_time=datetime.datetime.now(tz=datetime.timezone.utc),
                brand_id=1,
                item_id=item_id,
                category_id=1,
                bar_qr_code= "test",
                supplier_id=1,
                image_url="http://example.com/img")
        assert isinstance(resp, int)

    def test_remove(self):
        data = Items().create(
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
        item_id = data[0]
        resp = Items().remove(item_id=item_id)
        assert resp == None

    def test_get(self):
        resp = Items().get(organisation_name='test')
        assert len(resp) >= 0
    
    def test_get_with_item_list(self):
        resp = Items().get_with_item_list(organisation_name='test',item_code_list=['test'])
        assert len(resp) >= 0
    
    def test_remove_from_list(item_ids: list):
        data = Items().create(
                name="hqwel",
                description="test description",
                created_time=datetime.datetime.now(tz=datetime.timezone.utc),
                bar_qr_auto=True,
                organisation_id=1,
                brand_id=1,
                category_id=1,
                organisation_name= "neworg",
                bar_qr_code= "test",
                supplier_id=1,
                image_url="http://example.com/img"
            )
        item_id = data[0]
        resp = Items().remove_from_list(item_ids=[item_id])
        assert resp == None


        
