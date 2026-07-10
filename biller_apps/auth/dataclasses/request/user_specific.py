from dataclasses import dataclass


@dataclass
class UserSpecificData:
    organisationName: str
    name: str
    employeeCode: str
    emailId: str
    profilePhotoUrl: str
    shopAccessList: list
    approval: bool
