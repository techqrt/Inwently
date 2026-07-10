
from django.urls import reverse

class Endpoints:
    login = reverse('login')
    token = reverse('token')
    employees_get_all = reverse('employee_get_all')
    employees_get = reverse('employee_get')
    employees_create = reverse('employee_create')
    employees_search = reverse('employee_search')
    employees_update = reverse('employee_update')
    employee_delete = reverse('employee_delete')
    employees_delete_many = reverse('employee_delete_many')
    brand_create = reverse('brand_create')
    brand_get_all = reverse('brand_get_all')
    brand_delete = reverse('brand_delete')
    brand_update = reverse('brand_update')
    brand_delete_many = reverse('brand_delete_many')
    category_create = reverse('category_create')
    category_get_all = reverse('category_get_all')
    category_delete = reverse('category_delete')
    category_update = reverse('category_update')
    category_delete_many = reverse('category_delete_many')