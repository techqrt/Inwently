from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.return_item.controller import ReturnItemViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('return_item_create')
        self.assertEqual(resolve(url).func, ReturnItemViewController.create)

    def test_get_all(self):
        url = reverse('return_item_get_all')
        self.assertEqual(resolve(url).func, ReturnItemViewController.get_all)

    def test_get(self):
        url = reverse('return_item_get')
        self.assertEqual(resolve(url).func, ReturnItemViewController.get)

    def test_delete(self):
        url = reverse('return_item_delete')
        self.assertEqual(resolve(url).func, ReturnItemViewController.delete)

    def test_update(self):
        url = reverse('return_item_update')
        self.assertEqual(resolve(url).func, ReturnItemViewController.update)

    def test_search(self):
        url = reverse('return_item_search')
        self.assertEqual(resolve(url).func, ReturnItemViewController.search)
    
    def test_get_by_bill(self):
        url = reverse('return_item_get_by_bill')
        self.assertEqual(resolve(url).func, ReturnItemViewController.get_by_bill)

    def test_get_all(self):
        url = reverse('return_item_get_all')
        self.assertEqual(resolve(url).func, ReturnItemViewController.get_all)