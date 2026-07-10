from django.urls import path

from biller_apps.customer.controller import CustomerViewController

urlpatterns = [
    path('create/', CustomerViewController.create, name='customer_create'),
    path('get_all/', CustomerViewController.get_all, name='customer_get_all'),
    path('get/', CustomerViewController.get, name='customer_get'),
    path('update/', CustomerViewController.update, name='customer_update'),
    path('delete/', CustomerViewController.delete, name='customer_delete'),
    path('search/', CustomerViewController.search, name='customer_search'),
    path('delete_many/', CustomerViewController.delete_many, name='customer_delete_many'),
]
