from django.urls import path

from biller_apps.app_template.controller import AppTemplateViewController

urlpatterns = [
    path('create/', AppTemplateViewController.create, name='app_template_create'),
    path('get_all/', AppTemplateViewController.get_all, name='app_template_get_all'),
    path('delete/', AppTemplateViewController.delete, name='app_template_delete'),
    path('update/', AppTemplateViewController.update, name='app_template_update'),
    path('delete_many/', AppTemplateViewController.delete_many, name='app_template_delete_many'),
    path('search/', AppTemplateViewController.search, name='app_template_search'),

]
