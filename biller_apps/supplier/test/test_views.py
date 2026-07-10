import json
import datetime
from django.urls import reverse
from rest_framework import status

from biller_apps.supplier.serializers.request.create import SupplierRequest
from biller_apps.supplier.dataclasses.request.delete import SupplierDelete
from biller_apps.supplier.dataclasses.request.delete_many import SupplierDeleteManyRequest
from biller_apps.supplier.dataclasses.request.update import SupplierUpdate
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.supplier.dataclasses.request.get import SuppliersGet

from biller_apps.supplier.views import SupplierView
from biller_apps.supplier.models import Supplier
from biller_apps.organisation.models import Organisation
from biller_apps.common.models.adress import Address


from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.test_setup import TestSetUp

class TestSupplierViews(TestSetUp):
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
    
    
    

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='')
        resp = SupplierView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_search_extract(self):
        obj = Search(key="Test", page_num=1, limit=10)
        resp = SupplierView().search_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_get_extract(self):
        obj = SuppliersGet(supplier_code="T_1",values="")
        resp = SupplierView().get_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

   
    
    def test_update_extract(self):
        organisation = Organisation.objects.get(organisation_id=self.organisation_id)
        supplier = Supplier()
        supplier1 = supplier.create(
            name="Old Supplier",
            organisation_name=organisation.company_name,
            organisation_id=self.organisation_id,
            mobile_number="9876543210",
            email_id="supplier@example.com",
            alt_mobile_number="9876543211",
            id_number="123456789",
            id_type="Aadhar",
            gst_number="22AAAAA0000A1Z5",
            photo_url="http://example.com/photo.jpg",
            id_proof_url="http://example.com/id_proof.jpg",
            address_id=self.address_id  # Use self.address_id instead of self.address.id
        )
        
        supplier_obj = Supplier.objects.get(supplier_id=supplier1)
        self.token_payload.organisation_id = self.organisation_id  
        self.token_payload.organisationName = organisation.company_name 

        obj = SupplierUpdate(
            name="Updated Supplier",
            state="New State",
            country="New Country",
            street="New Street",
            mobile_number="9123456789",
            email_id="updated@example.com",
            alt_mobile_number="9123456790",
            id_number="987654321",
            id_type="PAN",
            gst_number="33BBBBB1111B2Z6",
            photo_url="http://example.com/new_photo.jpg",
            id_proof_url="http://example.com/new_id_proof.jpg",
            supplier_code=supplier_obj.supplier_code
        )

        resp = SupplierView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    

    
    
    def test_create_extract(self):
        organisation = Organisation.objects.get(organisation_id=self.organisation_id)

        obj = SupplierRequest(
            name="New Supplier",
            state="Test State",
            country="Test Country",
            street="Test Street",
            mobile_number="9876543210",
            email_id="supplier@test.com",
            alt_mobile_number="9876543211",
            id_number="123456789",
            id_type="Aadhar",
            gst_number="22AAAAA0000A1Z5",
            photo_url="http://example.com/photo.jpg",
            id_proof_url="http://example.com/id_proof.jpg"
        )

        self.token_payload.organisation_id = self.organisation_id
        self.token_payload.organisationName = organisation.company_name

        resp = SupplierView().create_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_delete_extract(self):
        
        organisation = Organisation.objects.get(organisation_id=self.organisation_id) 
        address_id = Address().create(state="kerala", street="kuruppam", country="India")
        supplier = Supplier().create(
            name="Old Supplier",
            organisation_name=organisation.company_name,  
            organisation_id=organisation.organisation_id,
            mobile_number="9876543210",
            email_id="supplier@example.com",
            alt_mobile_number="9876543211",
            id_number="123456789",
            id_type="Aadhar",
            gst_number="22AAAAA0000A1Z5",
            photo_url="http://example.com/photo.jpg",
            id_proof_url="http://example.com/id_proof.jpg",
            address_id=address_id 
        )
        supplier_obj = Supplier.objects.get(supplier_id=supplier)
        obj = SupplierDelete(supplier_code=supplier_obj.supplier_code)
        self.token_payload.organisation_id = organisation.organisation_id
        self.token_payload.organisationName = organisation.company_name
        resp = SupplierView().delete_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)


    def test_delete_many(self):
        # Create multiple addresses
        
        #address_id2 = Address().create(state="kerala", street="Aloor", country="India")

        # Create organisations
        self.address_id_org = Address().create(state="kerala", street="kuruppam", country="India")

        self.address_id1 = Address().create(state="kerala", street="kuruppam", country="India")
        self.address_id2= Address().create(state="kerla", street="kuruppam", country="India")
        self.organisation_id1 = Organisation().create(
            owner_name="test1", owner_mobile="1234567890", company_name="test1",
            address_id=self.address_id_org, shop_count=1, employee_count=1,
            owner_alternate_mobile="", owner_email="testerpro1@gmail.com"
        )
        organisation1= Organisation.objects.get(organisation_id=self.organisation_id1) 
       
        # self.organisation_id2 = Organisation().create(
        #     owner_name="test2", owner_mobile="1234569890", company_name="test2",
        #     address_id=address_id2, shop_count=1, employee_count=1,
        #     owner_alternate_mobile="", owner_email="testerpro2@gmail.com"
        # )
        # organisation2= Organisation.objects.get(organisation_id=self.organisation_id2) 

        # Create suppliers
        supplier1 = Supplier().create(
            name="test2", organisation_name=organisation1.company_name,
            organisation_id=self.organisation_id1, mobile_number="9876543210",
            email_id="supplier1@example.com", alt_mobile_number="9876543211",
            id_number="123456789", id_type="Aadhar", gst_number="22AAAAA0000A1Z5",
            photo_url="http://example.com/photo1.jpg", id_proof_url="http://example.com/id_proof1.jpg",
            address_id=self.address_id1
        )
        

        supplier2 = Supplier().create(
            name="Supplier 2", organisation_name=organisation1.company_name,
            organisation_id=self.organisation_id1, mobile_number="9876543211",
            email_id="supplier2@example.com", alt_mobile_number="9876543212",
            id_number="123456790", id_type="Aadhar", gst_number="22AAAAA0000A1Z6",
            photo_url="http://example.com/photo2.jpg", id_proof_url="http://example.com/id_proof2.jpg",
            address_id=self.address_id2
        )

        # Retrieve supplier codes
        supplier_obj1 = Supplier.objects.get(supplier_id=supplier1)
        supplier_obj2 = Supplier.objects.get(supplier_id=supplier2)
        supplier_codes = [supplier_obj1.supplier_code, supplier_obj2.supplier_code]
        obj = SupplierDeleteManyRequest(supplier_code=supplier_codes)

        self.token_payload.organisation_id = organisation1.organisation_id
        self.token_payload.organisationName = organisation1.company_name
        resp = SupplierView().delete_many_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

        print("Testing with supplier codes:", supplier_codes)
        print("Response Status:", resp.status_code)
        print("Response Data:", resp.data)