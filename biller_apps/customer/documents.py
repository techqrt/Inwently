from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.customer.models import Customer


@registry.register_document
class CustomerDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'customer'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Customer
        fields = ['name']
