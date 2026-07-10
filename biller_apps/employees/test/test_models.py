import uuid

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.models.adress import Address
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees
from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops
from biller_apps.test_setup import TestSetUp
import datetime

class TestEmployeeModels(TestSetUp):
    def create_sample_employee(self,emp_id=2):
        address_id = Address().create(state="kerala", street="kuruppam", country="India")
        organisation_name = uuid.uuid4().hex[:10]
        organisation_id = Organisation().create(owner_name="test", owner_mobile=uuid.uuid4().hex[:10],
                                                     company_name=organisation_name,
                                                     address_id=address_id, shop_count=1, employee_count=1,
                                                     owner_alternate_mobile="", owner_email="testerpro@gmail.com",
                                                     plan_expiry=datetime.datetime.now(tz=datetime.timezone.utc))
        shop_id = Shops().create(name="test", organisation_name="test", organisation_id=organisation_id,
                                      address_id=address_id, website='-', email_id='-', mobile_number='-',
                                      alt_mobile_number='0', type='-')
        emp_cred_id = EmployeeCredentials().create(email_id=uuid.uuid4().hex[:10]+"@test.com", password="12345678")
        employee_id = Employees(employee_id=emp_id).create(name=organisation_name, mobile_number=uuid.uuid4().hex[:10],
                                                            address_id=address_id,
                                                            credentials_id=emp_cred_id,
                                                            dob=datetime.datetime(2020, 1, 1).date(),
                                                            organisation_id=organisation_id,
                                                            organisation_name=organisation_name, shop_access=[shop_id],
                                                            is_active=True, profile_photo_url='-',
                                                            dashboard_permission_id=1,
                                                            master_data_permission_id=1, inventory_permission_id=1,
                                                            sales_permission_id=1,
                                                            quotations_permission_id=1,
                                                            printer_templates_permission_id=1, purchase_permission_id=1,
                                                            reports_permission_id=1, token_key="test",
                                                            refresh_token="test",alternate_mobile_number=uuid.uuid4().hex[:10])
        return employee_id

    def test_create(self):
        resp = self.create_sample_employee(emp_id=3)
        assert isinstance(resp, int)

    def test_get_all(self):
        resp = Employees().get_all(organisation_name='test',params=GetAll(values='', page_num=1, sort_by='is_active', sort_order='asc', filter_key='', filter_value='',search_key='',limit=10))
        assert len(resp) >= 0

    def test_update(self):
        resp = Employees.update(employee_id=self.employee_id,name="test", mobile_number="702589665412",alternate_mobile_number="966656462123",dob=datetime.datetime(2020, 1, 1).date(),
                                shop_access=[self.shop_id],profile_photo_url="test")
        assert self.employee_id == resp

    def test_remove(self):
        resp = self.create_sample_employee(emp_id=5)
        new_resp = Employees.remove(employee_id=resp)
        assert new_resp == None

    def test_get_by_mobile(self):
        resp = Employees.get_by_mobile(mobile_number="1234567843",organisation_name="test")
        assert len(resp) >= 0
        

    def test_get_with_email(self):
        resp = Employees.get_with_email(email_id="test@gmail.com")
        assert resp is None


    def test_get_by_email_dob_code(self):
        resp = Employees.get_by_email_dob_code(employee_code="test", email_id="test2@example.com", dob=datetime.datetime(2003, 5, 15).date())
        assert resp is None

    def test_update_activation(self):
        resp = Employees.update_activation(employee_id=self.employee_id, is_active=True, email_verified=True)
        assert isinstance(resp,int)

    def test_get(self):
        resp = Employees.get(employee_code='test', organisation_name='test')
        assert resp is None

    def test_get_by_email(self):
        resp = Employees.get_by_email(email="test@example.com",organisation_name="test")
        assert resp is None

    def test_get_login_auth(self):
        resp = Employees.get_login_auth(employee_credentials_id=84)
        assert resp is None
        

    def test_update_tokens(self):
        resp = Employees.update_tokens(employee_id=self.employee_id,access_token="test",refresh_token="test",token_key="test")
        assert isinstance(resp,int)

    def test_get_by_id(self):
        resp = Employees.get_by_id(employee_credentials_id=84)
        assert resp is None

    def test_update_access_token(self):
        resp = Employees.update_access_token(employee_id=self.employee_id,access_token="test")
        assert resp is not None

    def test_get_count(self):
        resp = Employees.get_count(organisation_name="test")
        assert isinstance(resp, int)

    def test_get_with_code_list(self):
        resp = Employees.get_with_code_list(employee_code=[48,49],organisation_name="test")
        assert isinstance(resp,list)
    
    def test_get_by_id_except_one(self):
        resp = Employees.get_by_id_except_one(employee_id=self.employee_id, email_id="test@example.com")
        assert resp is None
    
    def test_get_by_refresh_token(self):
         resp = Employees.get_by_refresh_token(refresh_token="test")
         assert isinstance(resp,dict)

    def test_status_change_from_list(self):
         Employees.status_change_from_list(employee_id=[self.employee_id],status=True)
    
    def test_remove_from_list(self):
        emp_id = self.create_sample_employee(emp_id=4)
        Employees.remove_from_list(employee_id=[emp_id])
    


