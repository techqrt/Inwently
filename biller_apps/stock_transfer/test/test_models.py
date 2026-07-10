from biller_apps.stock_transfer.models import StockTransfer
from django.db.utils import IntegrityError
from biller_apps.test_setup import TestSetUp
from biller_apps.shops.models import Shops
from biller_apps.item.models.items import Items
from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation
import datetime

class TestStockTransferModels(TestSetUp):          
    def setUp(self):
        super().setUp()  
        
        self.address = Address().create(state="Kerala", street="Kuruppam", country="India")
        self.organisation = Organisation().create(address_id=self.address,company_name="test6",employee_count=2,owner_email="organistion@gmail.com",owner_mobile="9645154944",owner_name="owner1",shop_count=1)
        print(self.organisation)
        print()
        
        company_name = Organisation.objects.filter(organisation_id = self.organisation).values("company_name")
        print(company_name)
        
        self.shop_source = Shops().create(
            name="Shop A",organisation_name=Organisation.objects.filter(organisation_id = self.organisation).values("company_name"), organisation_id=self.organisation, address_id=self.address, 
            website="https://shopa.com", email_id="shopa@example.com",
            mobile_number="1234567890", alt_mobile_number="0987654321", type="Retail"
        )
        self.shop_dest = Shops().create(
            name="Shop B",organisation_name=Organisation.objects.filter(organisation_id = self.organisation).values("company_name"), organisation_id=self.organisation, address_id=self.address, 
            website="https://shopb.com", email_id="shopb@example.com",
            mobile_number="2345678901", alt_mobile_number="9876543210", type="Retail"
        )
        
        self.item = Items().create(
            name="test1", description="test", created_time=datetime.date(2020, 1, 1), 
             organisation_id=self.organisation,bar_qr_auto= False,bar_qr_code="123",organisation_name=Organisation.objects.filter(organisation_id = self.organisation).values("company_name"),
            category_id=1,supplier_id=1,brand_id=1
        )        
    def test_create_stock_transfer(self):
        resp = StockTransfer().create(
            source_shop_id=self.shop_source.shop_id,  
            destination_shop_id=self.shop_dest.shop_id, 
            item_id=self.item.item_id, 
            quantity=10,
            organisation_id=self.organisation,
            organisation_name=Organisation.objects.filter(organisation_id = self.organisation).values("company_name")
        )

        
        self.assertIsInstance(resp, int)
        
        
    def test_update(self):
        transfer_id = StockTransfer().create(
            source_shop_id=self.shop_source.shop_id, destination_shop_id=self.shop_dest.shop_id, item_id=self.item_id, quantity=10,
            organisation_id=self.organisation_id, organisation_name='TestOrg'
        )
        updated_id = StockTransfer.update(transfer_id, status='Completed', approved_by='Admin')
        assert updated_id == transfer_id
    
    

    # def test_get(self):
    #     transfer_id = StockTransfer().create(
    #         source_shop_id=self.shop_source.shop_id, destination_shop_id=self.shop_dest.shop_id, item_id=self.item_id, quantity=10,
    #         organisation_id=self.organisation_id, organisation_name='TestOrg'
    #     )
    #     resp = StockTransfer.get(organisation_name='TestOrg', transfer_code='T_1')
    #     assert resp is not None
    
    # def test_get_pending_transfers(self):
    #     resp = StockTransfer.get_pending_transfers(organisation_name='TestOrg')
    #     assert isinstance(resp, list)
    
    # def test_get_completed_transfers(self):
    #     resp = StockTransfer.get_completed_transfers(organisation_name='TestOrg')
    #     assert isinstance(resp, list)
    
    # def test_get_rejected_transfers(self):
    #     resp = StockTransfer.get_rejected_transfers(organisation_name='TestOrg')
    #     assert isinstance(resp, list)
    
    # def test_get_all(self):
    #     resp = StockTransfer.get_all(organisation_name='TestOrg')
    #     assert isinstance(resp, list)
    
    
    
    # def test_remove(self):
    #     transfer_id = StockTransfer().create(
    #         source_shop_id=1, destination_shop_id=2, item_id=1, quantity=10,
    #         organisation_id=self.organisation_id, organisation_name='TestOrg'
    #     )
    #     StockTransfer.remove(transfer_id)
    #     assert StockTransfer.objects.filter(transfer_id=transfer_id).count() == 0
    
    # def test_get_sorted_transfers_ascending(self):
    #     resp = StockTransfer.get_sorted_transfers(organisation_name='TestOrg', sort_order='asc')
    #     print(f"Type of resp: {type(resp)}, Value: {resp}")  
    #     assert isinstance(resp, list)


    # def test_get_sorted_transfers_descending(self):
    #     # Create test shops
    #     source_shop = Shops().create(shop_id=1, name="Shop1")
    #     destination_shop = Shops.objects.create(shop_id=2, name="Shop2")

    #     # Create test item
    #     item = Items.objects.create(item_id=1, name="Item1")

    #     # Create stock transfer
    #     StockTransfer().create(
    #         source_shop_id=source_shop.shop_id,
    #         destination_shop_id=destination_shop.shop_id,
    #         item_id=item.item_id,
    #         quantity=10,
    #         organisation_id=self.organisation_id,
    #         organisation_name="Test"
    #     )

    #     # Fetch sorted transfers
    #     resp = StockTransfer.get_sorted_transfers("Test", "desc")

    #     # Convert QuerySet to list and check
    #     assert isinstance(list(resp), list)
    #     assert len(resp) > 0
    