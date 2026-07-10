from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.organisation.models import Organisation 


@registry.register_document
class OrganisationDocument(Document):

    class Index:
        name = 'organisation'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Organisation
        fields = [
            'organisation_id',
            'company_name',
        ]
