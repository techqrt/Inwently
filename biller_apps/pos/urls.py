# biller_apps/pos/urls.py
from django.urls import path
from biller_apps.pos.controller import POSViewController

urlpatterns = [
    path('create', POSViewController.create, name='pos-create'),
    path('update', POSViewController.update, name='pos-update'),
    path('send', POSViewController.send, name='pos-send'),
    path('confirm', POSViewController.confirm, name='pos-confirm'),
    path('cancel', POSViewController.cancel, name='pos-cancel'),
    path('inventory-confirm', POSViewController.inventory_confirm, name='pos-inventory-confirm'),
    path('dispatch-add-details', POSViewController.dispatch_add_details, name='pos-dispatch-add-details'),
    path('dispatch-confirm', POSViewController.dispatch_confirm, name='pos-dispatch-confirm'),
    path('execute', POSViewController.execute, name='pos-execute'),
    path('get', POSViewController.get, name='pos-get'),
    path('get-all', POSViewController.get_all, name='pos-get-all'),
    path('delete', POSViewController.delete, name='pos-delete'),
]