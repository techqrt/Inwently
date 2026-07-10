import jwt
from django.urls import reverse
import datetime
from django.utils.timezone import make_aware
from biller.settings import SECRET_KEY
from biller_apps.test_setup import TestSetUp

from biller_apps.stock.models.stock import Stock
from biller_apps.shops.models import Shops
from biller_apps.employees.models.employees import Employees

from biller_apps.approvals.models import Approvals
class TestController(TestSetUp):
    def test_web_count(self):
        res = self.client.get(reverse('dashboard_web_count'), headers=self.header)
        self.assertEqual(res.status_code, 200)
