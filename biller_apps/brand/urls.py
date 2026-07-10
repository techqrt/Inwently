from django.urls import path

from biller_apps.brand.controller import BrandViewController

urlpatterns = [
    path('create/', BrandViewController.create, name='brand_create'),
    path('get_all/', BrandViewController.get_all, name='brand_get_all'),
    path('delete/', BrandViewController.delete, name='brand_delete'),
    path('update/', BrandViewController.update, name='brand_update'),
    path('delete_many/', BrandViewController.delete_many, name='brand_delete_many'),
    path('search/', BrandViewController.search, name='brand_search'),

]
