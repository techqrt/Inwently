import json
from django.urls import reverse
from rest_framework import status
import datetime

from biller_apps.status.models import Status   #importing model class
from biller_apps.test_setup import TestSetUp

from biller_apps.status.views import StatusView  #importing status view
from biller_apps.status.serializers.request.get import StatusGet

class TestStatusView(TestSetUp):
    def test_get_extract(self):
            obj = StatusGet(status_id=1)
            resp = StatusView().get_extract(params=obj)
            self.assertEqual(resp.status_code, 200)