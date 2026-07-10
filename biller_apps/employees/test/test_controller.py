from django.urls import reverse

from biller_apps.employees.models.employees import Employees
from biller_apps.test_setup import TestSetUp


class TestEmployeeController(TestSetUp):

    def test_get_all(self):
        res = self.client.get(reverse('employee_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        res = self.client.delete(reverse('employee_delete') + f'?employee_code=t_01', headers=self.header)
        self.assertEqual(res.status_code, 400)

    def test_update(self):
        empl_code = Employees.objects.filter(organisation_id=self.organisation_id).first().employee_code
        payload = {
          "name": "string12",
          "mobile_number": "string31",
          "alternate_mobile_number": "string34",
          "dob": "2025-02-18",
          "shop_access": [
            "test"
          ],
          "email_id": "user6@example.com",
          "state": "string",
          "country": "string",
          "street": "string",
          "profile_photo_url": "string",
          "permissions": {
            "master": {
              "item": True,
              "shop": True,
              "supplier": True,
              "customer": True,
              "create": True,
              "employee": True
            },
            "inventory": {
              "inventory": True
            },
            "billing": {
              "bill_history": True,
              "pos": True,
              "return_item": True
            },
            "reports": {
              "overview": True,
              "general": True,
              "administration": True,
              "day_book": True,
              "gst": True
            },
            "printer_templates": {
              "printer_templates": True
            },
            "dashboard": {
              "dashboard": True
            },
            "stock": {
              "stock": True,
              "purchase_list": True,
              "return_purchase": True
            },
            "quotations": {
              "quotations": True
            }
          },
          "employee_code": empl_code
        }
        resp = self.client.put(reverse('employee_update'), payload, format="json", headers=self.header)
        print('test update',resp.data)
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        payload = {
          "name": "string1",
          "mobile_number": "string1",
          "alternate_mobile_number": "string2",
          "dob": "2025-02-18",
          "shop_access": [
            "test"
          ],
          "email_id": "user1@example.com",
          "state": "string",
          "country": "string",
          "street": "string",
          "profile_photo_url": "string",
          "permissions": {
            "master": {
              "item": True,
              "shop": True,
              "supplier": True,
              "customer": True,
              "create": True,
              "employee": True
            },
            "inventory": {
              "inventory": True
            },
            "billing": {
              "bill_history": True,
              "pos": True,
              "return_item": True
            },
            "reports": {
              "overview": True,
              "general": True,
              "administration": True,
              "day_book": True,
              "gst": True
            },
            "printer_templates": {
              "printer_templates": True
            },
            "dashboard": {
              "dashboard": True
            },
            "stock": {
              "stock": True,
              "purchase_list": True,
              "return_purchase": True
            },
            "quotations": {
              "quotations": True
            }
          }
        }
        res = self.client.post(reverse('employee_create'), payload, format="json", headers=self.header)
        print('test create',res.json())
        self.assertEqual(res.status_code, 201)

    def test_search(self):
        res = self.client.get(reverse('employee_search') + '?key=test', headers=self.header)
        self.assertEqual(res.status_code, 200)
