from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.purchase.controller import PurchaseViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('purchase_create')
        self.assertEqual(resolve(url).func, PurchaseViewController.create)

    def test_get_all(self):
        url = reverse('purchase_get_all')
        self.assertEqual(resolve(url).func, PurchaseViewController.get_all)

    def test_get(self):
        url = reverse('purchase_get')
        self.assertEqual(resolve(url).func, PurchaseViewController.get)

    def test_delete(self):
        url = reverse('purchase_delete')
        self.assertEqual(resolve(url).func, PurchaseViewController.delete)

    def test_update(self):
        url = reverse('purchase_update')
        self.assertEqual(resolve(url).func, PurchaseViewController.update)

    def test_search(self):
        url = reverse('purchase_search')
        self.assertEqual(resolve(url).func, PurchaseViewController.search)
