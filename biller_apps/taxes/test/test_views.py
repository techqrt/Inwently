import json
from django.urls import reverse
from rest_framework import status
import datetime

#from biller_apps.taxes.serializers.request.create import TaxesCreateSerializer
from biller_apps.taxes.dataclases.request.create import TaxesCreate
from biller_apps.taxes.dataclases.request.update import TaxesUpdate
from biller_apps.taxes.dataclases.request.delete_many import TaxesDeleteMany
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.taxes.views import TaxesView
from biller_apps.taxes.models import Taxes
from biller_apps.organisation.models import Organisation

from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.test_setup import TestSetUp

class TestTaxesViews(TestSetUp):
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
                    {"name": "koratty", "shopCode": "T_1"}
                ],
                "approval": False
            },
            "permissions": {}
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
    
    def test_create_extract(self):
        obj = TaxesCreate(name="New Tax", total_tax=18.0, tax_splits={"cgst": 9.0, "sgst": 9.0})
        resp = TaxesView().create_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)  
 
        # resp = TaxesView().create_extract(params=tax_request, token_payload=self.token_payload)
        # self.assertEqual(resp.status_code, 201)

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='',search_key="")
        resp = TaxesView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_search_extract(self):
        obj = Search(key="name", page_num=1, limit=10)
        resp = TaxesView().search_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_update_extract(self):
        organisation = Organisation.objects.get(organisation_id=self.organisation_id)
        tax = Taxes()
        tax1 = tax.create(name="Old Tax Name", total_tax=5.0, tax_splits={"cgst": 2.5, "sgst": 2.5}, organisation_id=self.organisation_id, organisation_name=organisation.company_name)
        tax_obj = Taxes.objects.get(tax_id=tax1)
        
        self.token_payload.organisation_id = self.organisation_id  
        self.token_payload.organisationName = organisation.company_name 
        obj = TaxesUpdate(tax_code=tax_obj.tax_code, name="Updated Tax", total_tax=10.0, tax_splits={"cgst": 5.0, "sgst": 5.0})
        resp = TaxesView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_delete_many_extract(self):
        organisation = Organisation.objects.get(organisation_id=self.organisation_id)
        tax1 = Taxes()
        tax_id1 = tax1.create(name="Tax 1", total_tax=12.0, tax_splits={"cgst": 6.0, "sgst": 6.0}, organisation_id=self.organisation_id, organisation_name=organisation.company_name)
        tax2 = Taxes()
        tax_id2 = tax2.create(name="Tax 2", total_tax=18.0, tax_splits={"cgst": 9.0, "sgst": 9.0}, organisation_id=self.organisation_id, organisation_name=organisation.company_name)
        
        tax_obj1 = Taxes.objects.get(tax_id=tax_id1)
        tax_obj2 = Taxes.objects.get(tax_id=tax_id2)
        
        self.token_payload.organisation_id = self.organisation_id  
        self.token_payload.organisationName = organisation.company_name  
        obj = TaxesDeleteMany(tax_codes=[tax_obj1.tax_code, tax_obj2.tax_code])
        resp = TaxesView().delete_many_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)
