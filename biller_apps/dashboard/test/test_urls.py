from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.dashboard.controller import DashboardController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('dashboard_web_count')
        self.assertEqual(resolve(url).func, DashboardController.web_count)