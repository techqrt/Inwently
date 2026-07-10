from django.urls import path

from biller_apps.status.controller import StatusController

urlpatterns = [
    path('get/', StatusController.get, name='status_get'),
]
