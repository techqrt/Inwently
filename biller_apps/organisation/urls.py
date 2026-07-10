from django.urls import path

from biller_apps.organisation.controller import OrganisationViewController

urlpatterns = [
    path('create/', OrganisationViewController.create, name='org_create'),
    path('get/', OrganisationViewController.get, name='org_get'),
    path('get_all/', OrganisationViewController.get_all, name='org_get_all'),
    path('delete/', OrganisationViewController.delete, name='org_delete'),
    path('delete_many/', OrganisationViewController.delete_many, name='org_delete_many'),
    path('update/', OrganisationViewController.update, name='org_update'),
    path('search/',OrganisationViewController.search,name='org_search'),
    path('update/', OrganisationViewController.update, name='org_update'),
    path('version/', OrganisationViewController.update_version, name='update_version'),
]
