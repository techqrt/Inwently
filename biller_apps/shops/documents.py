from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.shops.models import Shops


@registry.register_document
class SupplierDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'shops'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Shops
        fields = ['name']
