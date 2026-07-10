from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.shops.controller import ShopsViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('shop_create')
        self.assertEqual(resolve(url).func, ShopsViewController.create)


    def test_get_all(self):
        url = reverse('shop_get_all')
        self.assertEqual(resolve(url).func, ShopsViewController.get_all)

    def test_delete(self):
        url = reverse('shop_delete')
        self.assertEqual(resolve(url).func, ShopsViewController.delete)

    def test_update(self):
        url = reverse('shop_update')
        self.assertEqual(resolve(url).func, ShopsViewController.update)
    
    def test_search(self):
        url = reverse('shop_search')
        self.assertEqual(resolve(url).func, ShopsViewController.search)
    
    def test_delete_many(self):
        url = reverse('shop_delete_many')
        self.assertEqual(resolve(url).func, ShopsViewController.delete_many)
    
    def test_get(self):
        url = reverse('shop_get')
        self.assertEqual(resolve(url).func, ShopsViewController.get)
    
