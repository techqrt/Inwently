from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.organisation.controller import OrganisationViewController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('org_create')
        self.assertEqual(resolve(url).func, OrganisationViewController.create)

    def test_get(self):
        url = reverse('org_get')
        self.assertEqual(resolve(url).func, OrganisationViewController.get)

    def test_get_all(self):
        url = reverse('org_get_all')
        self.assertEqual(resolve(url).func, OrganisationViewController.get_all)

    def test_delete(self):
        url = reverse('org_delete')
        self.assertEqual(resolve(url).func, OrganisationViewController.delete)

    def test_update(self):
        url = reverse('org_update')
        self.assertEqual(resolve(url).func, OrganisationViewController.update)
    
    def test_delete_many(self):
        url = reverse('org_delete_many')
        self.assertEqual(resolve(url).func, OrganisationViewController.delete_many)