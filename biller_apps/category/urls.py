from django.urls import path

from biller_apps.category.controller import CategoryViewController

urlpatterns = [
    path('create/', CategoryViewController.create, name='category_create'),
    path('get_all/', CategoryViewController.get_all, name='category_get_all'),
    path('delete/', CategoryViewController.delete, name='category_delete'),
    path('update/', CategoryViewController.update, name='category_update'),
    path('delete_many/', CategoryViewController.delete_many, name='category_delete_many'),
    path('search/', CategoryViewController.search, name='category_search'),
]
