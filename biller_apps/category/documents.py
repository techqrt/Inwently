from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.category.models import Category


@registry.register_document
class BrandDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'category'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Category
        fields = ['name']
