import jwt
from django.urls import reverse

from biller.settings import SECRET_KEY
from biller_apps.category.models import Category
from biller_apps.category.views import CategoryView
from biller_apps.test_setup import TestSetUp


class TestCategoryViews(TestSetUp):

    def test_get_all(self):
        res = self.client.get(reverse('category_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        category_code = Category().create(name='testc1', organisation_id=self.organisation_id,
                                          organisation_name=self.organization_name)
        code = 't_' + str(category_code)
        res = self.client.delete(reverse('category_delete') + '?category_code='+ code,
                                 headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        category_code = Category().create(name='testc',organisation_id=self.organisation_id,organisation_name=self.organization_name)
        payload = {"name": "test", "category_code": 't_'+str(category_code)}
        res = self.client.put(reverse('category_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        payload = {"name": "test123"}
        res = self.client.post(reverse('category_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)
