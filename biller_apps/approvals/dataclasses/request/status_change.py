from dataclasses import dataclass


@dataclass
class ApprovalsStatusChangeRequest:
    approval_code: str
    approved: bool
