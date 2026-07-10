from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.quotations.controller import QuotationViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('quotation_create')
        self.assertEqual(resolve(url).func, QuotationViewController.create)

    def test_get_all(self):
        url = reverse('quotation_get_all')
        self.assertEqual(resolve(url).func, QuotationViewController.get_all)

    def test_get(self):
        url = reverse('quotation_get')
        self.assertEqual(resolve(url).func, QuotationViewController.get)

    def test_delete(self):
        url = reverse('quotation_delete')
        self.assertEqual(resolve(url).func, QuotationViewController.delete)

    def test_update(self):
        url = reverse('quotation_update')
        self.assertEqual(resolve(url).func, QuotationViewController.update)

    def test_search(self):
        url = reverse('quotation_search')
        self.assertEqual(resolve(url).func, QuotationViewController.search)
