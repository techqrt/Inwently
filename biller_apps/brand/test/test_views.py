import datetime

from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.brand.dataclasses.request.create import BrandRequest
from biller_apps.brand.dataclasses.request.delete import BrandDeleteRequest
from biller_apps.brand.dataclasses.request.delete_many import BrandDeleteManyRequest
from biller_apps.brand.dataclasses.request.update import BrandUpdateRequest
from biller_apps.brand.models import Brand
from biller_apps.brand.serializers.request.create import BrandRequestSerializer
from biller_apps.brand.views import BrandView
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.organisation.models import Organisation
from biller_apps.test_setup import TestSetUp


class TestBrandViews(TestSetUp):
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
                    "pos": True,
                    "return_item": True,
                    "bill_history": True
                },
                "reports": {
                    "general": True,
                    "overview": True,
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
                    "purchase_list": True,
                    "return_purchase": True,
                    "stock": True
                },
                "quotations": {
                    "quotations": True
                }
            }
        }

        user_data = token_data.get("user_specific_data", {})
        expiry_dt = datetime.datetime.strptime(token_data["expiry"], "%Y-%m-%d %H:%M:%S.%f%z")

        #  Pass correct fields to Payload
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

    def test_create_extract(self):
        obj = BrandRequestSerializer(data={"name": "New Brand"})
        obj.is_valid(raise_exception=True)
        validated_data = obj.validated_data
        brand_request = BrandRequest(**validated_data)

        resp = BrandView().create_extract(params=brand_request, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='',
                     search_key='')
        resp = BrandView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_search_extract(self):
        obj = Search(key="Test", page_num=1, limit=10)
        resp = BrandView().search_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_update_extract(self):
        organisation = Organisation.objects.get(organisation_id=self.organisation_id)
        brand = Brand()
        brand1 = brand.create(name="Old Brand Name", organisation_name=organisation.company_name, secure=False,
                              organisation_id=self.organisation_id)
        brand_obj = Brand.objects.get(brand_id=brand1)
        self.token_payload.organisation_id = self.organisation_id
        self.token_payload.organisationName = organisation.company_name
        obj = BrandUpdateRequest(brand_code=brand_obj.brand_code, name="Updated Brand")
        resp = BrandView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_many_extract(self):
        organisation = Organisation.objects.get(organisation_id=self.organisation_id)
        brand1 = Brand()
        brand_id1 = brand1.create(
            name="Brand 1",
            organisation_name=organisation.company_name,
            organisation_id=self.organisation_id,
            secure=False
        )

        brand2 = Brand()
        brand_id2 = brand2.create(
            name="Brand 2",
            organisation_name=organisation.company_name,
            organisation_id=self.organisation_id,
            secure=False
        )
        brand_obj1 = Brand.objects.get(brand_id=brand_id1)
        brand_obj2 = Brand.objects.get(brand_id=brand_id2)
        self.token_payload.organisation_id = self.organisation_id
        self.token_payload.organisationName = organisation.company_name
        obj = BrandDeleteManyRequest(brand_code=[brand_obj1.brand_code, brand_obj2.brand_code])
        resp = BrandView().delete_many_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        organisation = Organisation.objects.get(organisation_id=self.organisation_id)
        brand = Brand()
        brand_id = brand.create(
            name="Old Brand Name",
            organisation_name=organisation.company_name,
            organisation_id=self.organisation_id,
            secure=False
        )
        brand_obj = Brand.objects.get(brand_id=brand_id)
        self.token_payload.organisation_id = self.organisation_id
        self.token_payload.organisationName = organisation.company_name
        obj = BrandDeleteRequest(brand_code=brand_obj.brand_code)
        resp = BrandView().delete_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
