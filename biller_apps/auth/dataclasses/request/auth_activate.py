from dataclasses import dataclass

from biller_apps.employees.dataclasses.request.create import Permissions


@dataclass
class RegisterRequest:
    name: str
    mobile_number: str
    alternate_mobile_number: str
    dob: str
    shop_access: list
    email_id: str
    state: str
    country: str
    street: str
    profile_photo_url: str
    permissions: Permissions
    organisation_name: str
    password: str
