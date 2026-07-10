import datetime
from django.urls import reverse
from django.http import HttpRequest

from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.dashboard.views import DashboardView
from biller_apps.test_setup import TestSetUp
from rest_framework.request import Request


class TestDashboardViews(TestSetUp):
    def setUp(self):
        super().setUp()
        token_data = {
            "expiry": "2025-02-08 03:20:58.011817+0000",
            "user_specific_data": {
                "organisationName": "Techaso",
                "name": "Angel Mariya",
                "employeeCode": "T_12",
                "emailId": "angelmariya145@gmail.com",
                "profilePhotoUrl": "profile_photo_url",
                "shopAccessList": [
                    {
                        "name": "koratty",
                        "shopCode": "T_1"
                    }
                ],
                "approval": False
            },
            "permissions": {
                "dashboard": {
                    "dashboard": True
                }
            }
        }

        user_data = token_data.get("user_specific_data", {})
        expiry_dt = datetime.datetime.strptime(token_data["expiry"], "%Y-%m-%d %H:%M:%S.%f%z")

        self.token_payload = Payload(
            email_id=user_data.get("emailId", ""),
            expiry=expiry_dt,
            organisationName=user_data.get("organisationName", ""),
            organisation_id=self.organisation_id,
            present_url="",
            access_token="",
            method="",
            path="",
            approval=user_data.get("approval", False),
            permissions=token_data.get("permissions", {})
        )
    def test_web_count(self):
        django_request = HttpRequest()  
        request = Request(django_request) 
        resp = DashboardView().web_count(request)
        self.assertEqual(resp.status_code, 200)
        expected_keys = {"organisationCount", "shopsCount", "employeesCount", "deviceCount"}
        self.assertCountEqual(resp.data.keys(), expected_keys)