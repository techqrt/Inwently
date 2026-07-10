from django.urls import path

from biller_apps.employees.controller import EmployeesViewController

urlpatterns = [
    path('create/', EmployeesViewController.create, name='employee_create'),
    path('update/', EmployeesViewController.update, name='employee_update'),
    path('delete/', EmployeesViewController.delete, name='employee_delete'),
    path('get/', EmployeesViewController.get, name='employee_get'),
    path('get_all/', EmployeesViewController.get_all, name='employee_get_all'),
    path('delete_many/', EmployeesViewController.delete_many, name='employee_delete_many'),
    path('search/', EmployeesViewController.search, name='employee_search'),
    path('bulk_status_change/', EmployeesViewController.bulk_status_change, name='employee_bulk_status_change')


]
