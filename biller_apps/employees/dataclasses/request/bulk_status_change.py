from dataclasses import dataclass


@dataclass
class EmployeeBulkStatusChangeRequest:
    employee_code: list
    status: bool
