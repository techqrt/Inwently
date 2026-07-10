from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.taxes.models import Taxes


@registry.register_document
class TaxesDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'taxes'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Taxes
        fields = ['name']
