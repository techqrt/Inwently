from django.urls import path

from biller_apps.places.controller import PlaceViewController

urlpatterns = [
    path('get/', PlaceViewController.get, name='place_get'),
]
