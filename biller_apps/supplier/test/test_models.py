from biller_apps.supplier.models import Supplier
from biller_apps.test_setup import TestSetUp


class TestSupplierModels(TestSetUp):

    def test_create(self):
        resp = Supplier().create(name='test1', mobile_number='1234567816', email_id='test1@gmail.com',
                                 id_number='11110000', alt_mobile_number="09019212", id_type="aadhar",
                                 gst_number="xxxxx", photo_url="http://test", id_proof_url="http://checking",
                                 organisation_name="test", address_id=self.address_id,organisation_id=self.organisation_id)
        assert isinstance(resp, int)

    def test_get_all(self):
        resp = Supplier.get_all(organisation_name='test')
        assert len(resp) > 0

    def test_get(self):
        resp = Supplier.get(organisation_name='test', supplier_code='t_' + str(self.supplier_id))
        assert len(resp) > 0
        resp = Supplier().get(organisation_name='test', supplier_code='t_' + str(self.supplier_id), single=True)
        assert isinstance(resp, dict)

    def test_update(self):
        resp = Supplier.update(name='test', mobile_number='1234517816', email_id='test@gmail.com',
                               id_number='11110000', alt_mobile_number="090159212", id_type="aadhar",
                               gst_number="xxxxx", photo_url="http://test",
                               id_proof_url="http://checking", supplier_id=self.supplier_id)
        assert isinstance(resp, int)

    def test_remove(self):
        resp = Supplier.remove(supplier_id=self.supplier_id)
        assert resp is None
        
    def test_get_by_email(self):
        supplier_id = Supplier().create(
            name='test_mobile', mobile_number='9876543210', email_id='test_mobile@gmail.com',
            id_number='22223333', alt_mobile_number="0987654321", id_type="passport",
            gst_number="GST12345", photo_url="http://photo", id_proof_url="http://idproof",
            organisation_name="test_org", address_id=self.address_id, organisation_id=self.organisation_id
        )
        stored_org_name = Supplier.objects.get(email_id='test_mobile@gmail.com').organisation_id.company_name
        resp = Supplier.get_by_email(organisation_name=stored_org_name,email='test_mobile@gmail.com')
        assert isinstance(resp, dict)

    def test_get_with_code_list(self):
        resp = Supplier.get_with_code_list(supplier_code=['t_1', 't_2'], organisation_name='test')
        assert isinstance(resp, list)

    def test_remove_from_list(self):
        resp = Supplier.remove_from_list(supplier_codes=['t_1', 't_2'])
        assert resp is None

    def test_get_sorted_suppliers(self):
        resp = list(Supplier.get_sorted_suppliers(organisation_name='test', sort_order='asc'))
        assert isinstance(resp, list)

    def test_get_by_mobile(self):
        supplier_id = Supplier().create(
            name='test_mobile', mobile_number='9876543210', email_id='test_mobile@gmail.com',
            id_number='22223333', alt_mobile_number="0987654321", id_type="passport",
            gst_number="GST12345", photo_url="http://photo", id_proof_url="http://idproof",
            organisation_name="test_org", address_id=self.address_id, organisation_id=self.organisation_id
        )
        stored_org_name = Supplier.objects.get(mobile_number="9876543210").organisation_id.company_name
        resp = Supplier.get_by_mobile(organisation_name=stored_org_name, mobile_number="9876543210")
        assert isinstance(resp, dict)
