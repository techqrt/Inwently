import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from biller_apps.billing.models.customer_bills import CustomerBills
from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.common.models.adress import Address
from biller_apps.customer.models import Customer
from biller_apps.customer_quotation.models import CustomerQuotation
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees
from biller_apps.employees.models.permission import (
    DashboardPermission, DispatchPermission, InventoryPermission, MasterDataPermission,
    PrinterTemplatesPermission, PurchasePermission, QuotationsPermission, ReportsPermission,
    SalesPermission,
)
from biller_apps.inventory.models import Inventory
from biller_apps.item.models.items import Items
from biller_apps.organisation.models import Organisation
from biller_apps.pos.models import POS
from biller_apps.shops.models import Shops
from biller_apps.supplier.models import Supplier


class DirectCreationHTTPSmokeTests(APITestCase):
    """
    End-to-end HTTP smoke test through the real stack: login -> JWT ->
    AuthenticationMiddleware -> serializer -> controller -> view -> utils -> DB,
    for the two new additive workflows (direct PI, direct invoice) plus the
    existing quotation/PI/invoice flows they must not disturb.
    """

    def setUp(self):
        self.address_id = Address().create(state="kerala", street="mg road", country="India")
        self.organisation_name = "SmokeOrg"
        self.organisation_id = Organisation().create(
            owner_name="test", owner_mobile="1234567890", company_name=self.organisation_name,
            address_id=self.address_id, shop_count=1, employee_count=1, owner_alternate_mobile="",
            owner_email="owner@smoke.com", plan_expiry=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        self.shop_id = Shops().create(
            name="Main", organisation_name=self.organisation_name, organisation_id=self.organisation_id,
            address_id=self.address_id, website="-", email_id="-", mobile_number="-",
            alt_mobile_number="0", type="-",
        )
        self.shop = Shops.objects.get(shop_id=self.shop_id)

        self.brand_id = Brand().create(name="B", organisation_name=self.organisation_name, organisation_id=self.organisation_id)
        self.category_id = Category().create(name="C", organisation_id=self.organisation_id, organisation_name=self.organisation_name)
        self.supplier_id = Supplier().create(
            name="S", mobile_number="1234500000", email_id="supplier@smoke.com",
            id_number="111", alt_mobile_number="222", id_type="aadhar", gst_number="gst123",
            photo_url="", id_proof_url="", organisation_name=self.organisation_name,
            address_id=self.address_id, organisation_id=self.organisation_id,
        )
        self.item_id, self.item_code = Items().create(
            name="Item", description="desc", organisation_name=self.organisation_name,
            bar_qr_code="bq1", organisation_id=self.organisation_id, brand_id=self.brand_id,
            category_id=self.category_id, supplier_id=self.supplier_id, image_url="",
            tax_id=None, hsn_code="h1",
        )
        Inventory.objects.create(
            item_id_id=self.item_id, shop_id=self.shop, organisation_id_id=self.organisation_id,
            balance_qty=50,
        )

        self.customer_id = Customer().create(
            name="Walk-in Customer", mobile_number="9999900000",
            organisation_name=self.organisation_name, organisation_id=self.organisation_id,
            address_id=self.address_id,
        )
        self.customer = Customer.objects.get(customer_id=self.customer_id)

        self.emp_cred_id = EmployeeCredentials().create(email_id="admin@smoke.com", password="password123")
        self.employee_id = Employees().create(
            name="Admin", mobile_number="8888800000", address_id=self.address_id,
            credentials_id=self.emp_cred_id, dob=datetime.date(1990, 1, 1),
            organisation_id=self.organisation_id, organisation_name=self.organisation_name,
            shop_access=[self.shop_id], is_active=True, profile_photo_url="-",
            dashboard_permission_id=DashboardPermission().create(dashboard=True),
            master_data_permission_id=MasterDataPermission().create(
                item=True, supplier=True, shop=True, customer=True, employee=True, create=True
            ),
            inventory_permission_id=InventoryPermission().create(inventory=True),
            sales_permission_id=SalesPermission().create(pos=True, return_item=True, bill_history=True),
            quotations_permission_id=QuotationsPermission().create(quotations=True),
            printer_templates_permission_id=PrinterTemplatesPermission().create(printer_templates=True),
            purchase_permission_id=PurchasePermission().create(purchase_list=True, return_purchase=True, stock=True),
            reports_permission_id=ReportsPermission().create(
                general=True, overview=True, administration=True, day_book=True, gst=True
            ),
            dispatch_permission_id=DispatchPermission().create(dispatch=True),
        )

        auth = self.client.post(
            reverse('login'), {"email_id": "admin@smoke.com", "password": "password123"}, format="json"
        )
        self.assertEqual(auth.status_code, status.HTTP_200_OK, auth.data)
        self.header = {'HTTP_AUTHORIZATION': 'Bearer ' + auth.data['data']['access_token']}

    def test_direct_pi_creation_over_http(self):
        response = self.client.post(
            '/pos/create', {
                "customer_code": self.customer.customer_code,
                "shop_code": self.shop.shop_code,
                "items": [{"item_code": self.item_code, "quantity": 2, "price": "100.00", "tax": "10.00", "discount": "0.00"}],
            }, format="json", **self.header,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        pos_id = response.data['data']['pos_id']
        pos = POS.objects.get(pos_id=pos_id)
        self.assertIsNone(pos.customer_quotation_id)

    def test_direct_invoice_creation_over_http(self):
        response = self.client.post(
            '/billing/create/', {
                "customer_name": "Walk-in Customer",
                "customer_phone": "9999900000",
                "items": [{"item_code": self.item_code, "quantity": 3, "price": "50.00", "tax": "0.00", "discount": "0.00"}],
            }, format="json", **self.header,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        customer_bills = CustomerBills.objects.get(customer_bills_id=response.data['data']['customer_bills_id'])
        self.assertIsNone(customer_bills.pos_id)
        self.assertEqual(customer_bills.customer_name, "Walk-in Customer")

    def test_existing_quotation_to_pi_to_invoice_over_http(self):
        quotation_resp = self.client.post(
            '/customer-quotation/create', {
                "customer_name": "Phone Customer", "customer_phone": "7777700000",
                "shop_code": self.shop.shop_code,
                "items": [{"item_code": self.item_code, "quantity": 1}],
            }, format="json", **self.header,
        )
        self.assertEqual(quotation_resp.status_code, status.HTTP_200_OK, quotation_resp.data)
        quotation_code = quotation_resp.data['data']['customer_quotation_code']

        Customer().create(
            name="Phone Customer", mobile_number="7777700000",
            organisation_name=self.organisation_name, organisation_id=self.organisation_id,
            address_id=self.address_id,
        )

        quotation = CustomerQuotation.objects.get(customer_quotation_code=quotation_code)
        review_resp = self.client.put(
            '/customer-quotation/review', {
                "customer_quotation_id": quotation.customer_quotation_id,
                "status": CustomerQuotation.STATUS_PHONE_CONFIRMED,
            }, format="json", **self.header,
        )
        self.assertEqual(review_resp.status_code, status.HTTP_200_OK, review_resp.data)

        quotation.refresh_from_db()
        self.assertEqual(quotation.status, CustomerQuotation.STATUS_CONVERTED)

        pos = POS.objects.get(customer_quotation_id=quotation.customer_quotation_id)

        self.assertEqual(
            self.client.put('/pos/confirm', {"pos_id": pos.pos_id}, format="json", **self.header).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.put('/pos/inventory-confirm', {"pos_id": pos.pos_id}, format="json", **self.header).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.put(
                '/pos/dispatch-add-details',
                {"pos_id": pos.pos_id, "logistics_company": "Smoke Logistics", "logistics_charges": "10.00"},
                format="json", **self.header,
            ).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.put('/pos/dispatch-confirm', {"pos_id": pos.pos_id}, format="json", **self.header).status_code,
            status.HTTP_200_OK,
        )
        execute_resp = self.client.post('/pos/execute', {"pos_id": pos.pos_id}, format="json", **self.header)
        self.assertEqual(execute_resp.status_code, status.HTTP_200_OK, execute_resp.data)

        pos.refresh_from_db()
        self.assertEqual(pos.status, POS.STATUS_EXECUTED)
