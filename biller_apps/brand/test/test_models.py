from biller_apps.brand.models import Brand
from biller_apps.test_setup import TestSetUp


class TestBrandModels(TestSetUp):
    def test_create(self):
        resp = Brand().create(name='test', organisation_name='test', secure=False, organisation_id=self.organisation_id)
        assert isinstance(resp, int)

    def test_create_secure_brand(self):
        resp = Brand().create(name='test', organisation_name='test', secure=True, organisation_id=self.organisation_id)
        assert isinstance(resp, int)

    def test_get(self):
        brand1 = Brand().create(name="Brand1", organisation_name="test", secure=False,
                                organisation_id=self.organisation_id)
        resp = Brand.get(organisation_name='test')
        assert len(resp) >= 0

    def test_get_with_code(self):
        brand_id = Brand().create(name="Brand1", organisation_name="test", secure=False,
                                  organisation_id=self.organisation_id)
        brand1 = Brand.objects.get(brand_id=brand_id)
        resp = Brand.get_with_code(brand_code=brand1.brand_code, organisation_name="test")
        assert resp is not None

    def test_get_with_code_list(self):
        resp = Brand.get_with_code_list(brand_code=["t_1", "t_2"], organisation_name="test1")
        assert len(resp) >= 0

    def test_remove(self):
        brand1 = Brand().create(name="Brand1", organisation_name="test1", secure=False,
                                organisation_id=self.organisation_id)
        Brand.remove(brand1)
        assert Brand.objects.filter(brand_id=brand1).count() == 0

    def test_remove_from_list(self):
        brand1 = Brand().create(name="Brand1", organisation_name="test1", secure=False,
                                organisation_id=self.organisation_id)
        brand2 = Brand().create(name="Brand2", organisation_name="test2", secure=False,
                                organisation_id=self.organisation_id)
        Brand.remove_from_list([brand1, brand2])
        assert Brand.objects.filter(brand_id__in=[brand1, brand2]).count() == 0

    def test_get_sorted_brands_ascending(self):
        resp = Brand.get_sorted_brands("Test", "asc")
        assert resp is not None

    def test_get_sorted_brands_descending(self):
        resp = Brand.get_sorted_brands("Test", "desc")
        assert resp is not None

    def test_update(self):
        brand1 = Brand()
        brand1_id = brand1.create(name="Brand1", organisation_name="test1", secure=False,
                                  organisation_id=self.organisation_id)
        brand1_obj = Brand.objects.get(brand_id=brand1_id)
        payload = {
            "brand_id": brand1_obj.brand_code,
            "name": "Updated Name"
        }
        brand1_obj.name = payload["name"]
        brand1_obj.save()
        updated_brand = Brand.objects.get(brand_id=brand1_obj.brand_id)
        self.assertEqual(updated_brand.name, "Updated Name")
