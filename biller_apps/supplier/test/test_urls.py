from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.supplier.controller import SupplierViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('supplier_create')
        self.assertEqual(resolve(url).func, SupplierViewController.create)

    def test_get(self):
        url = reverse('supplier_get')
        self.assertEqual(resolve(url).func, SupplierViewController.get)

    def test_get_all(self):
        url = reverse('supplier_get_all')
        self.assertEqual(resolve(url).func, SupplierViewController.get_all)

    def test_delete(self):
        url = reverse('supplier_delete')
        self.assertEqual(resolve(url).func, SupplierViewController.delete)

    def test_update(self):
        url = reverse('supplier_update')
        self.assertEqual(resolve(url).func, SupplierViewController.update)

    def test_search(self):
        url = reverse('supplier_search')
        self.assertEqual(resolve(url).func, SupplierViewController.search)

    def test_delete_many(self):
        url = reverse('supplier_delete_many')
        self.assertEqual(resolve(url).func, SupplierViewController.delete_many)
