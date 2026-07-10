import datetime


from django.urls import reverse
from rest_framework.test import APITestCase

from biller_apps.billing.models.billing import Billing
from biller_apps.common.models.adress import Address
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees
from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops
from biller_apps.supplier.models import Supplier
from biller_apps.quotations.models import Quotation

from biller_apps.return_item.models import ReturnItem
from biller_apps.brand.models import Brand
from biller_apps.purchase.models import Purchase
from biller_apps.category.models import Category
from biller_apps.item.models.items import Items
from biller_apps.taxes.models import Taxes

from biller_apps.item.models.item_version import ItemVersion





class TestSetUp(APITestCase):
    def setUp(self):
        self.address_id = Address().create(state="kerala", street="kuruppam", country="India")
        self.address_id_1 = Address().create(state="kerala", street="kuruppam", country="India")
        self.organization_name = 'test'
        self.organisation_id = Organisation().create(owner_name="test", owner_mobile="1234567890", company_name=self.organization_name,
                                                     address_id=self.address_id, shop_count=1, employee_count=1,owner_alternate_mobile="",owner_email="testerpro@gmail.com",plan_expiry=datetime.datetime.now(tz=datetime.timezone.utc))
        self.shop_id = Shops().create(name="test", organisation_name="test", organisation_id=self.organisation_id,
                                 address_id=self.address_id, website='-', email_id='-', mobile_number='-',
                                 alt_mobile_number='0', type='-')
        self.shop_id_2 = Shops().create(name="test", organisation_name="test", organisation_id=self.organisation_id,
                                 address_id=self.address_id, website='-', email_id='-', mobile_number='-',
                                 alt_mobile_number='0', type='-')
        self.emp_cred_id = EmployeeCredentials().create(email_id="test@test.com", password="12345678")
        self.employee_id = Employees(employee_id = 10).create(name="test", mobile_number="1234567843", address_id=self.address_id,
                           credentials_id=self.emp_cred_id, dob=datetime.datetime(2020, 1, 1).date(),
                           organisation_id=self.organisation_id, organisation_name="test", shop_access=[self.shop_id],
                           is_active=True, profile_photo_url='-', dashboard_permission_id=1,
                           master_data_permission_id=1, inventory_permission_id=1, sales_permission_id=1,
                           quotations_permission_id=1, printer_templates_permission_id=1, purchase_permission_id=1,
                           reports_permission_id=1,token_key="test",refresh_token="test")
        self.brand_id = Brand().create(name="test", organisation_name= "test", organisation_id= self.organisation_id)
        self.category_id = Category().create(name= "test", organisation_id= self.organisation_id, organisation_name= "test")
        self.supplier_id = Supplier().create(name='test', mobile_number='1234517816', email_id='test@gmail.com',
                                             id_number='11110000', alt_mobile_number="090159212", id_type="aadhar",
                                             gst_number="xxxxx", photo_url="http://test",
                                             id_proof_url="http://checking",organisation_name="test", address_id=self.address_id_1,organisation_id=self.organisation_id)
        self.tax_id = Taxes().create(name='test', total_tax=10.5, tax_splits={'cgst': 5.0, 'sgst': 5.5}, organisation_id=self.organisation_id, organisation_name='test', secure=False)

        
        self.item_id = Items().create(name="test", description= "test", organisation_name= "test",
                                    bar_qr_code= "test", organisation_id= self.organisation_id, brand_id=self.brand_id, category_id= self.category_id, supplier_id= self.supplier_id,
                                    image_url= "http://example.com/img",tax_id=self.tax_id,hsn_code="t1")
        self.quotation_id = Quotation().create(supplier_id=self.supplier_id,organisation_id=self.organisation_id,organisation_name='test',
                                    item_id=self.item_id[0],description='Test Description',brand='Test Brand',quantity=10.0,
                                    price=200.0,tax=20.0,purchase=True,sales=False)
        self.bill_id,self.bill_number = Billing(billing_id = 1).create(created_at=datetime.datetime.now(tz=datetime.timezone.utc), employee_id= self.employee_id, item_id=self.item_id[0], organisation_id=self.organisation_id,
                                        shop_id=self.shop_id, quantity=10.0, mrp_price=10.0)

        self.purchase_id = Purchase(purchase_id = 20).create(purchase_bill_number= self.bill_number, supplier_id=self.supplier_id,
                                             item_id=self.item_id[0], buying_price=10.0,organisation_id=self.organisation_id, organisation_name="test", 
                                             landing_cost=10.0, selling_price=10.0,tax=10.0, quantity=10.0, bill_amount=10.0)
        self.return_item_id = ReturnItem().create(bill_id= self.bill_id, supplier_id= self.supplier_id, organisation_id= self.organisation_id, 
                                                item_id= self.item_id[0],organisation_name= "test",return_reason= "test", 
                                                quantity= 10.0,price= 200.0,tax= 10.0)
        self.item_version_id = ItemVersion().create(item_id=self.item_id[0],mrp_price=10.0,supplier_price=10.0,
                                                    created_time=datetime.datetime(2020, 1, 2).date(),added_by="test",unit="test",
                                                    expiry_date=datetime.date(2021, 2, 3),quantity=10.0)
        auth = self.client.post(reverse('login'), {"email_id": "test@test.com", "password": "12345678"}, format="json")
        self.header = {'Authorization': 'Bearer ' + auth.data['data']['access_token']}
        self.access_token = auth.data['data']['access_token']

        return super().setUp()

    def tearDown(self):
        return super().tearDown()