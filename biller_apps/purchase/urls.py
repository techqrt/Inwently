from django.urls import path

from biller_apps.purchase.controller import PurchaseViewController

urlpatterns = [
    path('create/', PurchaseViewController.create, name='purchase_create'),
    path('get_all/', PurchaseViewController.get_all, name='purchase_get_all'),
    path('get/', PurchaseViewController.get, name='purchase_get'),
    path('delete/', PurchaseViewController.delete, name='purchase_delete'),
    path('update/', PurchaseViewController.update, name='purchase_update'),
    path('search/', PurchaseViewController.search, name='purchase_search'),

]
