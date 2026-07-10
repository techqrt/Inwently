from dataclasses import dataclass


@dataclass
class StatusGetResponse:
    statusId: int
    status: str
    progress: int
