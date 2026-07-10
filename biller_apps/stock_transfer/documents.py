from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.stock_transfer.models import StockTransfer


@registry.register_document
class StockTransferDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'stock_transfer'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = StockTransfer
        fields = ['transfer_code']