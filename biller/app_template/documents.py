from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.app_template.models import AppTemplate


@registry.register_document
class AppTemplateDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'app_template'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = AppTemplate
        fields = [

        ]
