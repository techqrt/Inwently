from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.employees.controller import EmployeesViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('employee_create')
        self.assertEqual(resolve(url).func, EmployeesViewController.create)


    def test_get_all(self):
        url = reverse('employee_get_all')
        self.assertEqual(resolve(url).func, EmployeesViewController.get_all)

    def test_delete(self):
        url = reverse('employee_delete')
        self.assertEqual(resolve(url).func, EmployeesViewController.delete)

    def test_update(self):
        url = reverse('employee_update')
        self.assertEqual(resolve(url).func, EmployeesViewController.update)
    
    def test_get(self):
        url = reverse('employee_get')
        self.assertEqual(resolve(url).func, EmployeesViewController.get)
    
    def test_search(self):
        url = reverse('employee_search')
        self.assertEqual(resolve(url).func,EmployeesViewController.search)
    
    def test_bulk_status_change(self):
        url = reverse("employee_bulk_status_change")
        self.assertEqual(resolve(url).func,EmployeesViewController.bulk_status_change)

    def test_delete_many(self):
        url = reverse("employee_delete_many")
        self.assertEqual(resolve(url).func,EmployeesViewController.delete_many)
    
