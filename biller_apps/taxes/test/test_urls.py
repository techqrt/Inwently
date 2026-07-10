from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.taxes.controller import TaxesViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('taxes_create')
        self.assertEqual(resolve(url).func, TaxesViewController.create)

    def test_get_all(self):
        url = reverse('taxes_get_all')
        self.assertEqual(resolve(url).func, TaxesViewController.get_all)

    def test_update(self):
        url = reverse('taxes_update')
        self.assertEqual(resolve(url).func, TaxesViewController.update)

    def test_delete_many(self):
        url = reverse('taxes_delete_many')
        self.assertEqual(resolve(url).func, TaxesViewController.delete_many)

    def test_search(self):
        url = reverse('taxes_search')  # Ensure this name is correct in your urls.py
        self.assertEqual(resolve(url).func, TaxesViewController.search)
