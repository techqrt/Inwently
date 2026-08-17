# biller_apps/customer_quotation/urls.py
from django.urls import path
from biller_apps.customer_quotation.controller import CustomerQuotationViewController

urlpatterns = [
    path('create', CustomerQuotationViewController.create, name='customer-quotation-create'),
    path('review', CustomerQuotationViewController.review, name='customer-quotation-review'),
    path('get', CustomerQuotationViewController.get, name='customer-quotation-get'),
    path('get-all', CustomerQuotationViewController.get_all, name='customer-quotation-get-all'),
]