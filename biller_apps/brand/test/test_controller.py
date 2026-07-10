from django.urls import reverse

from biller_apps.brand.models import Brand
from biller_apps.test_setup import TestSetUp


# from biller_apps.organisation.models import Organisation


class TestBrandViewController(TestSetUp):

    def test_create(self):
        payload = {"name": "test123h"}
        res = self.client.post(reverse('brand_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)

    def test_get_all(self):
        res = self.client.get(reverse('brand_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        brand = Brand()
        brand_id = brand.create(name="Old Brand Name", organisation_name="test1", secure=False,
                                organisation_id=self.organisation_id)

        brand_obj = Brand.objects.get(brand_id=brand_id)
        payload = {
            "name": "Updated Brand Name",
            "brand_code": brand_obj.brand_code,
        }
        resp = self.client.put(reverse('brand_update'), data=payload, format="json", headers=self.header)
        self.assertEqual(resp.status_code, 200)

    def test_search(self):
        res = self.client.get(reverse('brand_search') + '?key=test', headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        brand = Brand()
        brand_id = brand.create(name="Brand1", organisation_name="test1", secure=False,
                                organisation_id=self.organisation_id)

        brand_obj = Brand.objects.get(brand_id=brand_id)
        res = self.client.delete(reverse('brand_delete') + '?brand_code=' + brand_obj.brand_code, headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_delete_many(self):
        brand1 = Brand()
        brand1_id = brand1.create(name="Brand1", organisation_name="test1", secure=False,
                                  organisation_id=self.organisation_id)

        brand2 = Brand()
        brand2_id = brand2.create(name="Brand2", organisation_name="test1", secure=False,
                                  organisation_id=self.organisation_id)

        brand1_obj = Brand.objects.get(brand_id=brand1_id)
        brand2_obj = Brand.objects.get(brand_id=brand2_id)
        payload = {
            "brand_code": [brand1_obj.brand_code, brand2_obj.brand_code]
        }
        res = self.client.patch(reverse('brand_delete_many'), data=payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)
