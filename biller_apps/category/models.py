import urllib
import uuid

from django.db import models
from django.db.models import Q

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.organisation.models import Organisation


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    category_code = models.CharField(max_length=50, default='', unique=True)
    secure = models.BooleanField(default=False)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category'

    def create(self, name: str, organisation_id: int, organisation_name: str, secure: bool = False) -> int:
        self.name = name
        self.organisation_id = Organisation(organisation_id)
        self.secure = secure
        if secure:
            code_id = str(uuid.uuid4())[-8:]
        else:
            self.save()
            code_id = self.category_id
        self.category_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(code_id)
        self.save()
        return self.category_id

    @staticmethod
    def get(organisation_name: str, params: GetAll):
        filters=Q(organisation_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_key=='is_active':
                filters= filters & Q(**{params.filter_key:params.filter_key.lower()=='true'})
            else:
                filters=filters & Q(**{params.filter_key:params.filter_value})
        if len(params.search_key)>0:
            filters=filters & Q(name__icontains=params.search_key)
        return Category.objects.filter(filters).values('name','category_code').order_by(params.ordering)

    @staticmethod
    def remove(category_id: int):
        Category.objects.get(category_id=category_id).delete()

    @staticmethod
    def get_with_code(category_code: str, organisation_name: str):
        return Category.objects.filter(category_code=category_code,
                                       organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'category_id').first()

    @staticmethod
    def update(category_id: int, name: str) -> int:
        category = Category.objects.get(category_id=category_id)
        category.name = name
        category.save()
        return category_id

    @staticmethod
    def remove_from_list(category_ids: list) -> None:
        Category.objects.filter(category_id__in=category_ids).delete()

    @staticmethod
    def get_with_code_list(category_code: list, organisation_name: str) -> list:
        return list(Category.objects.filter(category_code__in=category_code,
                                            organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'category_id'))

    @staticmethod
    def get_sorted_categories(organisation_name: str, sort_order: str) -> list:
        order_by = 'name' if sort_order == 'asc' else '-name'
        return Category.objects.filter(organisation_id__company_name=organisation_name).values('name',
                                                                                       'category_code').order_by(
            order_by)
