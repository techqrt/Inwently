from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class EmployeeGet(Get):
    employee_code: str


