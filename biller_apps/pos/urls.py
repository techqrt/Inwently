# biller_apps/pos/urls.py
from django.urls import path
from biller_apps.pos.controller import POSViewController

urlpatterns = [
    path('create', POSViewController.create, name='pos-create'),
    path('update', POSViewController.update, name='pos-update'),
    path('send', POSViewController.send, name='pos-send'),
    path('confirm', POSViewController.confirm, name='pos-confirm'),
    path('cancel', POSViewController.cancel, name='pos-cancel'),
    path('execute', POSViewController.execute, name='pos-execute'),
    path('get', POSViewController.get, name='pos-get'),
    path('get-all', POSViewController.get_all, name='pos-get-all'),
    path('delete', POSViewController.delete, name='pos-delete'),
]