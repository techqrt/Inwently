from unicodedata import category

from biller_apps.category.models import Category
from biller_apps.test_setup import TestSetUp


class TestCategoryModels(TestSetUp):

    def test_create(self):
        resp = Category().create(name='test1', organisation_name="test", organisation_id=self.organisation_id)
        assert isinstance(resp, int)

    def test_get_all(self):
        resp = Category().get(organisation_name='test')
        assert len(resp) > 0

    def test_update(self):
        category = Category().create(name='test3', organisation_name=self.organization_name, organisation_id=self.organisation_id)
        resp = Category.update(name='test34', category_id=category)
        assert isinstance(resp, int)

    def test_remove(self):
        category = Category().create(name='test3', organisation_name=self.organization_name,
                                     organisation_id=self.organisation_id)
        resp = Category.remove(category_id=category)
        assert resp is None
