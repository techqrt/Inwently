from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.places.controller import PlaceViewController


class TestUrls(SimpleTestCase):

    def test_get(self):
        url = reverse('place_get')
        self.assertEqual(resolve(url).func, PlaceViewController.get)
