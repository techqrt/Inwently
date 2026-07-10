from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.billing.models.customer_bills import CustomerBills



@registry.register_document
class BillingDocument(Document):
    organisation_id_id = fields.IntegerField()
    shop_id_id = fields.IntegerField()

    class Index:
        name = 'billing'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = CustomerBills
        fields = [
            'bill_number',
            'created_at'
        ]
