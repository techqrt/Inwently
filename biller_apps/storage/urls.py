from django.urls import path

from biller_apps.storage.controller import StorageViewController

urlpatterns = [
    path('upload/', StorageViewController.upload, name='storage_upload'),
    path('create/', StorageViewController.create, name='storage_create'),
    path('delete/', StorageViewController.delete, name='storage_delete'),
    path('get/', StorageViewController.get, name='storage_get'),
]
