from dataclasses import dataclass


@dataclass
class EmailVerify:
    email: str
    employee_code: str
