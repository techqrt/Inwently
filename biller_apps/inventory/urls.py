from django.urls import path

from biller_apps.inventory.controller import InventoryViewController

urlpatterns = [

    path('get_all/', InventoryViewController.get_all, name='inventory_get_all'),

]
