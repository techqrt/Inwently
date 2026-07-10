from django.urls import path

from biller_apps.return_item.controller import ReturnItemViewController

urlpatterns = [
    path('create/', ReturnItemViewController.create, name='return_item_create'),
    path('get_all/', ReturnItemViewController.get_all, name='return_item_get_all'),
    path('get/', ReturnItemViewController.get, name='return_item_get'),
    path('get_by_bill/', ReturnItemViewController.get_by_bill, name='return_item_get_by_bill'),
    path('delete/', ReturnItemViewController.delete, name='return_item_delete'),
    path('update/', ReturnItemViewController.update, name='return_item_update'),
    path('search/', ReturnItemViewController.search, name='return_item_search'),
]
