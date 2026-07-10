from django.urls import path

from biller_apps.shops.controller import ShopsViewController

urlpatterns = [
    path('create/', ShopsViewController.create, name='shop_create'),
    path('get_all/', ShopsViewController.get_all, name='shop_get_all'),
    path('delete/', ShopsViewController.delete, name='shop_delete'),
    path('update/', ShopsViewController.update, name='shop_update'),
    path('search/', ShopsViewController.search, name='shop_search'),
    path('delete_many/', ShopsViewController.delete_many, name='shop_delete_many'),
    path('get/', ShopsViewController.get, name='shop_get'),
]
