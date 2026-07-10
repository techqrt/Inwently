from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.customer.controller import CustomerViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('customer_create')
        self.assertEqual(resolve(url).func, CustomerViewController.create)

    def test_get_all(self):
        url = reverse('customer_get_all')
        self.assertEqual(resolve(url).func, CustomerViewController.get_all)

    def test_get(self):
        url = reverse('customer_get')
        self.assertEqual(resolve(url).func, CustomerViewController.get)

    def test_update(self):
        url = reverse('customer_update')
        self.assertEqual(resolve(url).func, CustomerViewController.update)

    def test_delete(self):
        url = reverse('customer_delete')
        self.assertEqual(resolve(url).func, CustomerViewController.delete)

    def test_search(self):
        url = reverse('customer_search')
        self.assertEqual(resolve(url).func, CustomerViewController.search)

    def test_delete_many(self):
        url = reverse('customer_delete_many')
        self.assertEqual(resolve(url).func, CustomerViewController.delete_many)
