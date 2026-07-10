from biller_apps.organisation.models import Organisation
from biller_apps.test_setup import TestSetUp


class TestModels(TestSetUp):

    def test_create(self):
        resp = Organisation().create(owner_name='test1', owner_mobile='1234567810', company_name='test1',
                                     address_id=self.address_id,shop_count=5,employee_count=5,approval=False,owner_alternate_mobile='1234567890',plan='CUSTOM',owner_email="testerproper@gmail.com")   
        assert isinstance(resp, int)

    def test_update(self):
        resp = Organisation.update(owner_name='test2', owner_mobile='1122334455', company_name='test',
                                   organisation_id=self.organisation_id,employee_count=6,shop_count=6,approval=False,owner_alternate_mobile='1234560890',plan='CUSTOM',owner_email="testerproper123@gmail.com",plan_expiry='2026-12-12')
        assert self.organisation_id == resp

    def test_get(self):
        resp = Organisation.get(company_name='test2')
        assert len(resp) >= 0
        
    def test_get_single(self):
        resp = Organisation.get(company_name='test2',single=True)
        assert len(resp) >= 0

    def test_get_all(self):
        resp = Organisation.get_all(organisation_name='test2')
        assert len(resp) >= 0

    def test_remove(self):
        org_id = Organisation().create(owner_name='test3', owner_mobile='1234563810', company_name='test3',
                                     address_id=self.address_id, shop_count=5, employee_count=5, approval=False,
                                     owner_alternate_mobile='1234167890', plan='CUSTOM',
                                     owner_email="test4rproper@gmail.com")
        resp = Organisation.remove(organisation_id=org_id)
        assert resp == None
    
    def test_remove_from_list(self):
        org_id = Organisation().create(owner_name='test3', owner_mobile='1234563810', company_name='test3',
                                       address_id=self.address_id, shop_count=5, employee_count=5, approval=False,
                                       owner_alternate_mobile='1234167890', plan='CUSTOM',
                                       owner_email="test4rproper@gmail.com")
        resp = Organisation.remove_from_list(organisation_ids=[org_id])
        assert resp == None