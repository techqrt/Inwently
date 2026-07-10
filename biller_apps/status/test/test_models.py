from django.db.utils import IntegrityError
from biller_apps.test_setup import TestSetUp
from biller_apps.status.models import Status

class TestStatus(TestSetUp):      
    def setUp(self):
        # Create a Status instance using Django ORM's create method
        self.status = Status.objects.create(
            uuid="1",
            status="Pending",
            progress=50
        )

    def test_get(self):
        resp = Status.get(status_id="1")
        self.assertTrue(isinstance(resp, dict) or resp is None)