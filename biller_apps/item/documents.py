from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.item.models.items import Items


@registry.register_document
class ItemsDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'items'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Items
        fields = ['name']
