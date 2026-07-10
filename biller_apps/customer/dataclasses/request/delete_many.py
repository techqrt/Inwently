from dataclasses import dataclass


@dataclass
class CustomerDeleteManyRequest:
    customer_code: list
