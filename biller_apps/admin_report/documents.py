from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.admin_report.models import AdminReport


@registry.register_document
class AdminReportDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'admin_report'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = AdminReport
        fields = [

        ]
