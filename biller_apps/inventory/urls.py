from django.urls import path

from biller_apps.inventory.controller import InventoryViewController

urlpatterns = [

    path('create/', InventoryViewController.create, name='inventory_create'),
    path('get/', InventoryViewController.get, name='inventory_get'),
    path('update/', InventoryViewController.update, name='inventory_update'),
    path('get_all/', InventoryViewController.get_all, name='inventory_get_all'),

]