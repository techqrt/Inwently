from django.urls import path

from biller_apps.quotations.controller import QuotationViewController

urlpatterns = [
    path('create/', QuotationViewController.create, name='quotation_create'),
    path('get_all/', QuotationViewController.get_all, name='quotation_get_all'),
    path('get/', QuotationViewController.get, name='quotation_get'),
    path('delete/', QuotationViewController.delete, name='quotation_delete'),
    path('update/', QuotationViewController.update, name='quotation_update'),
    path('search/', QuotationViewController.search, name='quotation_search'),
]
