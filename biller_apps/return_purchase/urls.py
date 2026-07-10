from django.urls import path

from biller_apps.return_purchase.controller import ReturnPurchaseViewController

urlpatterns = [
    path('create/', ReturnPurchaseViewController.create, name='return_purchase_create'),
    path('get_all/', ReturnPurchaseViewController.get_all, name='return_purchase_get_all'),
    path('get/', ReturnPurchaseViewController.get, name='return_purchase_get'),
    path('delete/', ReturnPurchaseViewController.delete, name='return_purchase_delete'),
    path('update/', ReturnPurchaseViewController.update, name='return_purchase_update'),
    path('search/', ReturnPurchaseViewController.search, name='return_purchase_search'),
]
