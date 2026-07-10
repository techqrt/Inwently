import jwt
from django.urls import reverse
import json

from biller.settings import SECRET_KEY
from biller_apps.status.controller import StatusController
from biller_apps.test_setup import TestSetUp
from biller_apps.status.models import Status
from rest_framework import status

class StatusController(TestSetUp):
    def test_get(self):
        res = self.client.get(reverse('status_get') + '?status_id=1', headers=self.header)
        self.assertEqual(res.status_code, 200)
