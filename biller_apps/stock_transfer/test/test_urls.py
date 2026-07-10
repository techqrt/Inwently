from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.stock_transfer.controller import StockTransferViewController


class TestStockTransferUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('stock_transfer_create')
        self.assertEqual(resolve(url).func, StockTransferViewController.create)

    def test_get_pending_transfers(self):
        url = reverse('get_pending_stock_transfer')
        self.assertEqual(resolve(url).func, StockTransferViewController.get_pending_transfers)

    def test_get_completed_transfers(self):
        url = reverse('get_completed_stock_transfer')
        self.assertEqual(resolve(url).func, StockTransferViewController.get_completed_transfers)

    def test_get_rejected_transfers(self):
        url = reverse('get_rejected_stock_transfer')
        self.assertEqual(resolve(url).func, StockTransferViewController.get_rejected_transfers)

    def test_get(self):
        url = reverse('stock_transfer_get')
        self.assertEqual(resolve(url).func, StockTransferViewController.get)

    def test_delete(self):
        url = reverse('stock_transfer_delete')
        self.assertEqual(resolve(url).func, StockTransferViewController.delete)

    def test_update(self):
        url = reverse('stock_transfer_update')
        self.assertEqual(resolve(url).func, StockTransferViewController.update)

    def test_search(self):
        url = reverse('stock_transfer_search')
        self.assertEqual(resolve(url).func, StockTransferViewController.search)
