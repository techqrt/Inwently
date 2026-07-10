import jwt
from django.urls import reverse
import datetime
from biller.settings import SECRET_KEY
from biller_apps.test_setup import TestSetUp


class TestPlacesViews(TestSetUp):

    def test_get(self):
        
        params = {'country': 'India', 'state': None}
        res = self.client.get(reverse('place_get'), data=params, headers=self.header)
        self.assertEqual(res.status_code, 200)