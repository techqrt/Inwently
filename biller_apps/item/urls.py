from django.urls import path

from biller_apps.item.controller import ItemController

urlpatterns = [
    path('create/', ItemController.create, name='item_create'),
    path('bulk_create/', ItemController.bulk_create, name='item_bulk_create'),
    path('update/', ItemController.update, name='item_update'),
    path('delete/', ItemController.delete, name='item_delete'),
    path('get_all/', ItemController.get_all, name='item_get_all'),
    path('search/', ItemController.search, name='item_search'),
    path('delete_many/', ItemController.delete_many, name='item_delete_many'),
    path('get/', ItemController.get, name='item_get'),
]
