from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from biller_apps.places.models.country import Country
from biller_apps.places.models.states import States


@registry.register_document
class StatesDocument(Document):
    class Index:
        name = 'states'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = States
        fields = [
            'country',
            'states',
        ]


@registry.register_document
class CountryDocument(Document):
    class Index:
        name = 'country'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Country
        fields = [
            'country'
        ]
