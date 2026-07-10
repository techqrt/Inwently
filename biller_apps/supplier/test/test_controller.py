import jwt
from django.urls import reverse
import json

from biller.settings import SECRET_KEY
from biller_apps.supplier.controller import SupplierViewController
from biller_apps.test_setup import TestSetUp
from biller_apps.supplier.models import Supplier
from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation


from rest_framework import status


class TestSupplierViewController(TestSetUp):

    def test_create(self):
        payload = {
            "name": "Test Supplier",
            "state": "Test State",
            "country": "Test Country",
            "street": "Test Street",
            "mobile_number": "1234567890",
            "alt_mobile_number": "0987654321",
            "email_id": "test@example.com",
            "id_number": "123456789",
            "id_type": "Passport",
            "gst_number": "GST123456",
            "photo_url": "http://example.com/photo.jpg",
            "id_proof_url": "http://example.com/id_proof.jpg"
        }
        res = self.client.post(reverse('supplier_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)
    
    def test_get_all(self):
        res = self.client.get(reverse('supplier_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    def test_get(self):
        res = self.client.get(reverse('supplier_get') + '?supplier_code=t_' + str(self.supplier_id),
                              headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    def test_search(self):
        res = self.client.get(reverse('supplier_search') + '?key=test', headers=self.header)
        self.assertEqual(res.status_code, 200)
 
    def test_update(self):
        payload = {"name": "test", "mobile_number": "1234517816", "email_id": "test@gmail.com",
                   "id_number": "11110000", "alt_mobile_number": "090159212", "id_type": "aadhar",
                   "gst_number": "xxxxx", "photo_url": "http://test", "id_proof_url": "http://checking",
                   "supplier_code": "t_" + str(self.supplier_id), "state": "tamilnadu", "country": "india",
                   "street": "kuruppam"}
        res = self.client.put(reverse('supplier_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)
   
    def test_delete(self):
        res = self.client.delete(reverse('supplier_delete') + '?supplier_code=t_' + str(self.supplier_id),
                                 headers=self.header)
        self.assertEqual(res.status_code, 200)
    
    
    def test_delete_many(self):        
        address_id2= Address().create(state="kerala", street="Aloor", country="India")
        address_id3 = Address().create(state="kerala",street="kuruppam",country="India")
        #print("address_id2   and   address_id3",address_id3,address_id2)
        supplier_1 = Supplier().create(
            name='test3', mobile_number='2234517818', email_id='test3@gmail.com',
            id_number='11110003', alt_mobile_number="190159213", id_type="aadhar",
            gst_number="xxxxx", photo_url="http://test3", id_proof_url="http://checking3",
            organisation_name="test", address_id=address_id3, organisation_id=self.organisation_id
        )
        print("wwwwwwwwwwwwwwwwwwwwwww",address_id3,address_id2)
        supplier_2 = Supplier().create(
            name='test2', mobile_number='1234517817', email_id='test2@gmail.com',
            id_number='11110002', alt_mobile_number="090159214", id_type="aadhar",
            gst_number="xxxxx", photo_url="http://test2", id_proof_url="http://checking2",
            organisation_name="test", address_id=address_id2, organisation_id=self.organisation_id
        )
        supplier_codes = ["t_" + str(supplier_1), "t_" + str(supplier_2)]
        data = {"supplier_code": supplier_codes}
        url = reverse('supplier_delete_many')
        response = self.client.patch(url, data, format="json", headers=self.header)
       
        print("Testing with supplier IDs:", supplier_codes)
        print("Response Status:", response.status_code)
        print("Response Data:", response.data)
        
        self.assertEqual(response.status_code, 200)