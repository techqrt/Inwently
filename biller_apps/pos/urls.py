from django.urls import path

from biller_apps.pos.controller import POSViewController

urlpatterns = [
    path('create/', POSViewController.create, name='pos_create'),
]
