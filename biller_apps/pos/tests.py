import datetime

from django.test import TestCase

from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.common.models.adress import Address
from biller_apps.customer.models import Customer
from biller_apps.customer_quotation.models import CustomerQuotation
from biller_apps.customer_quotation.utils import CustomerQuotationUtils
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.employees import Employees
from biller_apps.employees.models.permission import (
    DashboardPermission, DispatchPermission, InventoryPermission, MasterDataPermission,
    PrinterTemplatesPermission, PurchasePermission, QuotationsPermission, ReportsPermission,
    SalesPermission,
)
from biller_apps.item.models.items import Items
from biller_apps.organisation.models import Organisation
from biller_apps.pos.dataclasses.request.update import POSItemAddEntry
from biller_apps.pos.models import POS
from biller_apps.pos.utils import POSUtils
from biller_apps.shops.models import Shops
from biller_apps.supplier.models import Supplier


class POSDirectCreationTests(TestCase):
    """
    Covers Step 1 of the PI/Invoice enhancement: a Proforma Invoice (POS) must be
    creatable without a CustomerQuotation, and the existing quotation-driven path
    must keep working unchanged.
    """

    def setUp(self):
        self.address_id = Address().create(state="kerala", street="mg road", country="India")
        self.organisation_name = "TestOrg"
        self.organisation_id = Organisation().create(
            owner_name="test", owner_mobile="1234567890", company_name=self.organisation_name,
            address_id=self.address_id, shop_count=1, employee_count=1, owner_alternate_mobile="",
            owner_email="owner@test.com", plan_expiry=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        self.shop_id = Shops().create(
            name="Main", organisation_name=self.organisation_name, organisation_id=self.organisation_id,
            address_id=self.address_id, website="-", email_id="-", mobile_number="-",
            alt_mobile_number="0", type="-",
        )
        self.shop = Shops.objects.get(shop_id=self.shop_id)

        self.brand_id = Brand().create(name="TestBrand", organisation_name=self.organisation_name, organisation_id=self.organisation_id)
        self.category_id = Category().create(name="TestCategory", organisation_id=self.organisation_id, organisation_name=self.organisation_name)
        self.supplier_id = Supplier().create(
            name="TestSupplier", mobile_number="1234500000", email_id="supplier@test.com",
            id_number="111", alt_mobile_number="222", id_type="aadhar", gst_number="gst123",
            photo_url="", id_proof_url="", organisation_name=self.organisation_name,
            address_id=self.address_id, organisation_id=self.organisation_id,
        )
        self.item_id, self.item_code = Items().create(
            name="TestItem", description="desc", organisation_name=self.organisation_name,
            bar_qr_code="bq1", organisation_id=self.organisation_id, brand_id=self.brand_id,
            category_id=self.category_id, supplier_id=self.supplier_id, image_url="",
            tax_id=None, hsn_code="h1",
        )

        self.customer_id = Customer().create(
            name="Walk-in Customer", mobile_number="9999900000",
            organisation_name=self.organisation_name, organisation_id=self.organisation_id,
            address_id=self.address_id,
        )
        self.customer = Customer.objects.get(customer_id=self.customer_id)

        self.emp_cred_id = EmployeeCredentials().create(email_id="staff@test.com", password="password123")
        self.employee_id = Employees().create(
            name="Staff", mobile_number="8888800000", address_id=self.address_id,
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

    def test_create_pos_without_quotation_succeeds(self):
        """Direct PI creation — no customer_quotation_code supplied at all."""
        pos = POSUtils.create(
            customer_code=self.customer.customer_code,
            shop_code=self.shop.shop_code,
            organisation_id=self.organisation_id,
            organisation_name=self.organisation_name,
            items=[POSItemAddEntry(item_code=self.item_code, quantity=2, price=100, tax=10, discount=0)],
            billed_by=self.employee_id,
        )

        self.assertIsNone(pos.customer_quotation_id)
        self.assertEqual(pos.status, POS.STATUS_DRAFT)
        self.assertTrue(pos.pos_code)
        self.assertEqual(pos.amount, 220)

    def test_create_pos_from_quotation_still_works(self):
        """Existing quotation -> PI path must remain unaffected by direct creation support."""
        quotation = CustomerQuotationUtils.create(
            customer_name="Phone Customer", customer_phone=self.customer.mobile_number,
            shop_code=self.shop.shop_code,
            items=[POSItemAddEntry(item_code=self.item_code, quantity=1, price=0, tax=0, discount=0)],
            organisation_id=self.organisation_id, organisation_name=self.organisation_name,
        )
        quotation.status = CustomerQuotation.STATUS_PHONE_CONFIRMED
        quotation.save(update_fields=["status"])

        pos = POSUtils.create(
            customer_code=self.customer.customer_code,
            shop_code=self.shop.shop_code,
            organisation_id=self.organisation_id,
            organisation_name=self.organisation_name,
            items=[POSItemAddEntry(item_code=self.item_code, quantity=1, price=50, tax=0, discount=0)],
            billed_by=self.employee_id,
            customer_quotation_code=quotation.customer_quotation_code,
        )

        self.assertEqual(pos.customer_quotation_id, quotation.customer_quotation_id)
        quotation.refresh_from_db()
        self.assertEqual(quotation.status, CustomerQuotation.STATUS_CONVERTED)
