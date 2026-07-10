from django.urls import reverse
import datetime

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.models.adress import Address
from biller_apps.customer.serializers.request.create import CustomerRequest
from biller_apps.customer.serializers.request.delete import CustomerDelete
from biller_apps.customer.serializers.request.delete_many import CustomerDeleteManyRequest
from biller_apps.customer.serializers.request.get import CustomerGet
from biller_apps.customer.serializers.request.update import CustomerUpdateRequest
from biller_apps.customer.views import CustomerView
from biller_apps.test_setup import TestSetUp
from biller_apps.common.dataclasses.search import Search
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.customer.models import Customer


class TestCustomerViews(TestSetUp):
    def setUp(self):
        super().setUp()
        self.token_payload = Payload(
            organisationName="test",
            organisation_id=self.organisation_id,
            present_url="test_url",
            email_id="test@test.com",
            expiry=datetime.datetime.now(),
            access_token=self.access_token,
            method="GET",
            path="/test",
            approval=False,
            permissions=None
        )

    def test_get_extract(self):
        customer = Customer().create(
            name="test",
            mobile_number="012345679",
            email_id="test@example.com",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=self.address_id
        )
        created_customer = Customer.objects.get(customer_id=customer)
        
        obj = CustomerGet(customer_code=created_customer.customer_code, values='')
        resp = CustomerView().get_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_extract(self):
        obj = GetAll(limit=10, values='', page_num=1, sort_by='', sort_order='', filter_key='', filter_value='',search_key='')
        resp = CustomerView().get_all_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_create_extract(self):
        obj = CustomerRequest(
            name='test_customer', mobile_number='1234567890', email_id='test@example.com', id_number='ID123',
            id_type='PAN', photo_url='', id_proof_url='', state='TestState', country='TestCountry', street='TestStreet',
            blood_group='A+', date_of_birth='1990-01-01', education='Graduate', gender='M', martial_status='Single',
            occupation='Engineer', religion='None'
        )
        resp = CustomerView().create_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 201)

    def test_update_extract(self):
        customer = Customer().create(
            name="test",
            mobile_number="012345679",
            email_id="test@example.com",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=self.address_id
        )
        
        created_customer = Customer.objects.get(customer_id=customer)
        
        obj = CustomerUpdateRequest(
            customer_code=created_customer.customer_code,
            name='updated_name',
            mobile_number='9876543210',
            email_id='updated@example.com',
            id_number='T_111',
            id_type='AADHAR',
            photo_url='',
            id_proof_url='',
            state='UpdatedState',
            country='UpdatedCountry',
            street='UpdatedStreet',
            blood_group='B+',
            date_of_birth='1985-05-05',
            education='Postgraduate',
            gender='F',
            martial_status='Married',
            occupation='Doctor',
            religion='Hindu'
        )
        resp = CustomerView().update_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_extract(self):
        address = Address().create(street='teststreet', country='india', state='kerala')
        customer = Customer().create(
            name="test",
            mobile_number="012345679",
            email_id="test@example.com",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=address
        )
        
        created_customer = Customer.objects.get(customer_id=customer)
        
        obj = CustomerDelete(customer_code=created_customer.customer_code)
        resp = CustomerView().delete_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)

    def test_delete_many_extract(self):
        customer_codes = []
        for i in range(2):
            address = Address().create(street='teststreet', country='india', state='kerala')
            customer = Customer().create(
                name=f"test_{i}",
                mobile_number=f"01234567{i}",
                email_id=f"test{i}@example.com",
                organisation_name="test",
                organisation_id=self.organisation_id,
                address_id=address
            )
            created_customer = Customer.objects.get(customer_id=customer)
            customer_codes.append(created_customer.customer_code)
            
        obj = CustomerDeleteManyRequest(customer_code=customer_codes)
        resp = CustomerView().delete_many_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
    
    def test_search_extract(self):
        obj = Search(key='test_search', limit=10, page_num=1)
        resp = CustomerView().search_extract(params=obj, token_payload=self.token_payload)
        self.assertEqual(resp.status_code, 200)
