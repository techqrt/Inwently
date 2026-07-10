from django.urls import reverse

from biller_apps.common.models.adress import Address
from biller_apps.test_setup import TestSetUp
from biller_apps.customer.models import Customer


class TestCustomerController(TestSetUp):
    def test_get(self):
        customer = Customer().create(
            name="test",
            mobile_number="012345679",
            email_id="test@example.com",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=self.address_id
        )

        created_customer = Customer.objects.get(customer_id=customer)
        customer_code = created_customer.customer_code
        res = self.client.get(reverse('customer_get') + f'?customer_code={customer_code}', headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get_all(self):
        res = self.client.get(reverse('customer_get_all'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_create(self):
        payload = {
            "name": "Test User",
            "mobile_number": "1234567890",
            "email_id": "testuser@gmail.com",
            "id_number": "12345",
            "organisation_name": "test_org",
            "organisation_id": 1,
            "address_id": 1
        }
        resp = self.client.post(reverse('customer_create'), payload, format="json", headers=self.header)
        self.assertEqual(resp.status_code, 201)

    def test_update(self):
        customer = Customer().create(
            name="test",
            mobile_number="012345679",
            email_id="test@example.com",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=self.address_id
        )
        
        created_customer = Customer.objects.get(customer_id=customer)
        payload = {
            "customer_id": customer, 
            "customer_code": created_customer.customer_code,
            "name": "Updated Name",
            "mobile_number": "9876543210",
            "email_id": "updateduser@gmail.com",
            "id_number": "54321",
            "organisation_name": "test" 
        }
        
        resp = self.client.put(reverse('customer_update'), payload, format="json", headers=self.header)
        self.assertEqual(resp.status_code, 200)


    def test_delete(self):
        address = Address().create(street='teststreet', country='india', state='kerala')
        # Create test customer
        customer = Customer().create(
            name="test",
            mobile_number="9999999999",
            email_id="unique_test@example.com",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=address
        )

        created_customer = Customer.objects.get(customer_id=customer)
        
        # Send DELETE request with customer_code as a query parameter
        url = reverse('customer_delete') + f'?customer_code={created_customer.customer_code}'
        res = self.client.delete(url, headers=self.header)
        self.assertEqual(res.status_code, 200)


        
    def test_search(self):
        customer = Customer().create(
            name="test",
            mobile_number="1234567890",
            email_id="test@example.com",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=self.address_id
        )
        res = self.client.get(
            reverse('customer_search') + '?key=1234567890&limit=10&page_num=1', 
            headers=self.header
        )
        self.assertEqual(res.status_code, 200)

    def test_delete_many(self):
        customer_codes = []
        for i in range(3):
            address = Address().create(street='teststreet',country='india',state='kerala')
            customer = Customer().create(
                name=f"test_{i}",
                mobile_number=f"12345{i}7890",
                email_id=f"test{i}@example.com",
                organisation_name="test",
                organisation_id=self.organisation_id,
                address_id=address
            )
            created_customer = Customer.objects.get(customer_id=customer)
            customer_codes.append(created_customer.customer_code)


        payload = {"customer_code": customer_codes}
        res = self.client.patch(reverse('customer_delete_many'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)
