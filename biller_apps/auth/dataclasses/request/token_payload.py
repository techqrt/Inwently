from dataclasses import dataclass
from datetime import datetime

from biller_apps.employees.dataclasses.request.create import Permissions


@dataclass
class Payload:
    email_id: str
    expiry: datetime
    organisationName: str
    organisation_id: int
    present_url: str
    access_token: str
    method: str
    path: str
    approval: bool
    permissions: Permissions
    role: str = 'EMPLOYEE'
