from django.urls import path

from biller_apps.billing.controller import BillingViewController

urlpatterns = [
    path('create/', BillingViewController.create, name='billing_create'),
    path('get_all/', BillingViewController.get_all, name='billing_get_all'),
    path('get/', BillingViewController.get, name='billing_get'),
    path('delete/', BillingViewController.delete, name='billing_delete'),
]
