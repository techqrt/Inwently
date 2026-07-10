from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.purchase.models.purchase import Purchase
from biller_apps.purchase.models.purchase_bills import PurchaseBills


@registry.register_document
class PurchaseDocument(Document):
    organisation_id_id = fields.IntegerField()
    purchase_bill_number = fields.TextField(attr="purchase_bill.purchase_bill_number")
    item = fields.TextField(attr="item.name")
    class Index:
        name = 'purchase'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Purchase
