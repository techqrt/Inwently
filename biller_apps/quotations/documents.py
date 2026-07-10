from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.quotations.models import Quotation


@registry.register_document
class QuotationDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'quotation'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Quotation
        fields = ["quotation_code"]