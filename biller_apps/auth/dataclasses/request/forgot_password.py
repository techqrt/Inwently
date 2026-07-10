from dataclasses import dataclass
from datetime import datetime


@dataclass
class ForgotPassword:
    email_id: str
    email_otp : int
    new_password: str