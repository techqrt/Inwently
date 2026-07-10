from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.return_purchase.models import ReturnPurchase


@registry.register_document
class ReturnPurchaseDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'return_purchase'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = ReturnPurchase
        fields=["return_code"]
