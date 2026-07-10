from django.urls import path

from biller_apps.supplier.controller import SupplierViewController

urlpatterns = [
    path('create/', SupplierViewController.create, name='supplier_create'),
    path('get_all/', SupplierViewController.get_all, name='supplier_get_all'),
    path('get/', SupplierViewController.get, name='supplier_get'),
    path('delete/', SupplierViewController.delete, name='supplier_delete'),
    path('update/', SupplierViewController.update, name='supplier_update'),
    path('search/', SupplierViewController.search, name='supplier_search'),
    path('delete_many/', SupplierViewController.delete_many, name='supplier_delete_many'),

]
