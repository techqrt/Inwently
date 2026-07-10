from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.brand.controller import BrandViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('brand_create')
        self.assertEqual(resolve(url).func, BrandViewController.create)

    def test_get_all(self):
        url = reverse('brand_get_all')
        self.assertEqual(resolve(url).func, BrandViewController.get_all)

    def test_delete(self):
        url = reverse('brand_delete')
        self.assertEqual(resolve(url).func, BrandViewController.delete)

    def test_update(self):
        url = reverse('brand_update')
        self.assertEqual(resolve(url).func, BrandViewController.update)

    def test_delete_many(self):
        url = reverse('brand_delete_many')
        self.assertEqual(resolve(url).func, BrandViewController.delete_many)

    def test_search(self):
        url = reverse('brand_search')
        self.assertEqual(resolve(url).func, BrandViewController.search)
