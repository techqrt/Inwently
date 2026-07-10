from biller_apps.customer.models import Customer
from biller_apps.test_setup import TestSetUp
from datetime import date

class TestCustomerModels(TestSetUp):

    def test_create(self):
        resp = Customer().create(
                name="test",
                mobile_number="012345679",
                email_id="a@gmail.com",
                id_number="12",
                id_type=None,
                photo_url=None,
                id_proof_url=None,
                blood_group=None,
                date_of_birth=None,
                education=None,
                gender="M",
                martial_status=None,
                occupation="o",
                religion="o",
                organisation_name="test",
                organisation_id=self.organisation_id,
                address_id=self.address_id
            )
        assert isinstance(resp, int)

    def test_get_all(self):
        resp = Customer().get_all(organisation_name='Techaso')
        assert len(resp) > 0

    def test_get(self):
        resp = Customer().get(
            customer_code="TEST001",
            organisation_name="test"
        )
        assert resp is not None

    def test_update(self):
        resp = Customer.update(
                customer_id=1,
                name="test",
                mobile_number="012345679",
                email_id="a@gmail.com",
                id_number="12",
                id_type=None,
                photo_url="",
                id_proof_url=None,
                blood_group=None,
                date_of_birth=None,
                education=None,
                gender="M",
                martial_status=None,
                occupation="o",
                religion="o"
            )
        assert isinstance(resp, int)

    def test_remove(self):
        customer_id = Customer().create(
            name="test",
            mobile_number="012345679",
            email_id="a@gmail.com",
            id_number="12",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=self.address_id
        )
        resp = Customer.remove(customer_id=customer_id)
        assert resp is None
    
    def test_get_by_mobile(self):
        resp = Customer.get_by_mobile(organisation_name="test", mobile_number="012345679")
        assert isinstance(resp, dict) or resp is None

    def test_get_by_email(self):
        resp = Customer.get_by_email(organisation_name="test", email="a@gmail.com")
        assert isinstance(resp, dict) or resp is None
    
    def test_get_with_code_list(self):
        resp = Customer.get_with_code_list(customer_code=["TEST001"], organisation_name="test")
        assert isinstance(resp, list)

    def test_remove_from_list(self):
        customer_id = Customer().create(
            name="test",
            mobile_number="012345679",
            email_id="a@gmail.com",
            id_number="12",
            organisation_name="test",
            organisation_id=self.organisation_id,
            address_id=self.address_id
        )
        resp = Customer.remove_from_list(customer_id=[customer_id])
        assert resp is None

