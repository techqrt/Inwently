from django.urls import reverse
from rest_framework import status
from biller_apps.test_setup import TestSetUp
from biller_apps.stock_transfer.models import StockTransfer


class TestStockTransferViewController(TestSetUp):

    def test_create(self):
        payload = {
            "data": {
                "source_shop_id": 1,
                "destination_shop_id": 2,
                "item_id": 100,
                "quantity": 10,
                "transfer_date_time": "2025-02-16T12:00:00Z",
                "status": "Pending",
                "organisation_id": 1,
                "remarks": "Test transfer",
                "requested_by": "Test User"
            }
        }
        res = self.client.post(reverse('stock_transfer_create'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 201)

    def test_get_pending_transfers(self):
        res = self.client.get(reverse('stock_transfer_get_pending'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get_completed_transfers(self):
        res = self.client.get(reverse('stock_transfer_get_completed'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get_rejected_transfers(self):
        res = self.client.get(reverse('stock_transfer_get_rejected'), headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_get(self):
        stock_transfer = StockTransfer.objects.create(
            source_shop_id=1,
            destination_shop_id=2,
            item_id=100,
            quantity=10,
            transfer_code="ST1234"
        )
        res = self.client.get(reverse('stock_transfer_get') + f'?transfer_code={stock_transfer.transfer_code}', headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_search(self):
        res = self.client.get(reverse('stock_transfer_search') + '?key=ST1234', headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        stock_transfer = StockTransfer.objects.create(
            source_shop_id=1,
            destination_shop_id=2,
            item_id=100,
            quantity=10,
            transfer_code="ST1234"
        )
        payload = {
            "transfer_code": stock_transfer.transfer_code,
            "status": "Approved",
            "approved_by": "Manager"
        }
        res = self.client.put(reverse('stock_transfer_update'), payload, format="json", headers=self.header)
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        stock_transfer = StockTransfer.objects.create(
            source_shop_id=1,
            destination_shop_id=2,
            item_id=100,
            quantity=10,
            transfer_code="ST1234"
        )
        res = self.client.delete(reverse('stock_transfer_delete') + f'?transfer_code={stock_transfer.transfer_code}', headers=self.header)
        self.assertEqual(res.status_code, 200)
