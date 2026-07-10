from dataclasses import dataclass


@dataclass
class RegisterRequest:
    email_id: str
    password: str
    email_otp:int
