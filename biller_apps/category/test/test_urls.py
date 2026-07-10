from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.category.controller import CategoryViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('category_create')
        self.assertEqual(resolve(url).func, CategoryViewController.create)


    def test_get_all(self):
        url = reverse('category_get_all')
        self.assertEqual(resolve(url).func, CategoryViewController.get_all)

    def test_delete(self):
        url = reverse('category_delete')
        self.assertEqual(resolve(url).func, CategoryViewController.delete)

    def test_update(self):
        url = reverse('category_update')
        self.assertEqual(resolve(url).func, CategoryViewController.update)
