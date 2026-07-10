from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from biller_apps.employees.models.employees import Employees


@registry.register_document
class EmployeesDocument(Document):
    organisation_id_id = fields.IntegerField()

    class Index:
        name = 'employees'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Employees
        fields = [
            'name',
            'mobile_number',
            'is_active',
            'employee_code',
            'created_date_time',
            'dob',
            'profile_photo_url'
        ]
