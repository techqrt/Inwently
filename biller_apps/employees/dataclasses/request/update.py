import datetime
from dataclasses import dataclass
from dataclasses import fields
from biller_apps.employees.dataclasses.request.create import Permissions


@dataclass
class EmployeesUpdateRequest:
    name: str
    mobile_number: str
    alternate_mobile_number: str
    dob: datetime.datetime
    shop_access: list
    email_id: str
    state: str
    country: str
    street: str
    profile_photo_url: str
    permissions: Permissions
    employee_code: str



    @staticmethod
    def dict_to_dataclass(dataclass_type, data):
        if isinstance(data, dict):
            field_types = {f.name: f.type for f in fields(dataclass_type)}
            return dataclass_type(**{k: EmployeesUpdateRequest.dict_to_dataclass(field_types[k], v) for k, v in data.items()})
        elif isinstance(data, list):
            return [EmployeesUpdateRequest.dict_to_dataclass(dataclass_type.__args__[0], item) for item in data]
        else:
            return data
