from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.status.controller import StatusController


class TestStockTransferUrls(SimpleTestCase):
    def test_get(self):
        url = reverse('status_get')
        self.assertEqual(resolve(url).func, StatusController.get)

    