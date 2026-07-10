from dataclasses import dataclass


@dataclass
class PasswordChange:
    old_password: str
    new_password: str
