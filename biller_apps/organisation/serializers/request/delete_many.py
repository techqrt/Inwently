from rest_framework import serializers

from biller_apps.organisation.dataclasses.request.delete_many import OrganisationDeleteManyRequest


class OrganisationDeleteManySerializer(serializers.Serializer):
    organisation_id = serializers.ListField(required=True)

    def create(self, validated_data) -> OrganisationDeleteManyRequest:
        return OrganisationDeleteManyRequest(**validated_data)
