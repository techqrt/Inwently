from dataclasses import dataclass


@dataclass
class EmployeeDeleteManyRequest:
    employee_code: list

