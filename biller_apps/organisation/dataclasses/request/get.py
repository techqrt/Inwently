from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class OrganisationGet(Get):
    name: str

