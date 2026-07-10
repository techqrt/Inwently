from django.urls import reverse
from biller_apps.test_setup import TestSetUp


class TestController(TestSetUp):

    def test_get(self):
        res = self.client.get(reverse('org_get') + '?name=test', headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get_all(self):
        res = self.client.get(reverse('org_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        payload = {
            "owner_name": "test_owner1",
            "owner_mobile": "9417532325",
            "name": "test_company2",
            "state": "kerala",
            "country": "India",
            "street": "kuruppam",
            "shop_count": 0,
            "employee_count": 0,
            "owner_email": "testerproper1@gmail.com",
            "owner_alternate_mobile": "1234563820",
            "plan": "CUSTOM",
            "plan_expiry": "2026-12-12"
        }
        resp = self.client.post(reverse('org_create'), payload, format="json", headers=self.header)
        self.assertEqual(resp.status_code, 201)

    def test_update(self):
        payload = {
            "owner_name": "test_owner1",
            "owner_mobile": "9417532325",
            "name": "test",
            "state": "kerala",
            "country": "India",
            "street": "kuruppam",
            "shop_count": 5,
            "employee_count": 5,
            "owner_email":"testerproper@gmail.com",
            "owner_alternate_mobile":"1234567820",
            "plan":"CUSTOM",
            "plan_expiry":"2026-12-12"
        }
        resp = self.client.put(reverse('org_update'), payload, format="json", headers=self.header)
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        res = self.client.delete(reverse('org_delete') + '?name=test', headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_many(self):
        payload = {
            "organisation_id": [2]
        }
        res = self.client.patch(reverse('org_delete_many'),payload,format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)
        
        

