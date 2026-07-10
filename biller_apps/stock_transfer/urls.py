from django.urls import path

from biller_apps.stock_transfer.controller import StockTransferViewController

urlpatterns = [
    path('create/', StockTransferViewController.create, name='stock_transfer_create'),
    path('get_pending_transfers/', StockTransferViewController.get_pending_transfers, name='get_pending_stock_transfer'),
    path('get_completed_transfers/', StockTransferViewController.get_completed_transfers, name='get_completed_stock_transfer'),
    path('get_rejected_transfers/', StockTransferViewController.get_rejected_transfers, name='get_rejected_stock_transfer'),
    path('get/', StockTransferViewController.get, name='stock_transfer_get'),
    path('delete/', StockTransferViewController.delete, name='stock_transfer_delete'),
    path('update/', StockTransferViewController.update, name='stock_transfer_update'),
    path('search/', StockTransferViewController.search, name='stock_transfer_search'),
]