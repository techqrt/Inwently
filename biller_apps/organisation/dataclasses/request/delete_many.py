from dataclasses import dataclass


@dataclass
class OrganisationDeleteManyRequest:
    organisation_id: list
