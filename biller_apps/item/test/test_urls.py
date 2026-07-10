from django.test import SimpleTestCase
from django.urls import reverse, resolve

from biller_apps.item.controller import ItemController


class TestUrls(SimpleTestCase):
    def test_create(self):
        url = reverse('item_create')
        self.assertEqual(resolve(url).func, ItemController.create)


    def test_get_all(self):
        url = reverse('item_get_all')
        self.assertEqual(resolve(url).func, ItemController.get_all)

    def test_delete(self):
        url = reverse('item_delete')
        self.assertEqual(resolve(url).func, ItemController.delete)

    def test_update(self):
        url = reverse('item_update')
        self.assertEqual(resolve(url).func, ItemController.update)
    
    def test_bulk_create(self):
        url = reverse('item_bulk_create')
        self.assertEqual(resolve(url).func, ItemController.bulk_create)
    
    def test_search(self):
        url = reverse('item_search')
        self.assertEqual(resolve(url).func, ItemController.search)
    
    def test_delete_many(self):
        url = reverse('item_delete_many')
        self.assertEqual(resolve(url).func, ItemController.delete_many)
    
    def test_get(self):
        url = reverse('item_get')
        self.assertEqual(resolve(url).func, ItemController.get)
    
