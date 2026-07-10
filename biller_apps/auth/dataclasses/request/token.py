from dataclasses import dataclass

from biller_apps.auth.dataclasses.request.user_specific import UserSpecificData
from biller_apps.employees.dataclasses.request.create import Permissions


@dataclass
class TokenPayload:
    expiry: str
    user_specific_data: UserSpecificData
    permissions: Permissions
