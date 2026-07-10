from django.urls import path

from biller_apps.taxes.controller import TaxesViewController

urlpatterns = [
    path('create/', TaxesViewController.create, name='taxes_create'),
    path('get_all/', TaxesViewController.get_all, name='taxes_get_all'),
    path('update/', TaxesViewController.update, name='taxes_update'),
    path('delete_many/', TaxesViewController.delete_many, name='taxes_delete_many'),
    path('search/', TaxesViewController.search, name='taxes_search'),
]
