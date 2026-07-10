from dataclasses import dataclass


@dataclass
class LoginRequest:
    email_id: str
    password: str
