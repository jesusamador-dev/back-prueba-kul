from dataclasses import dataclass


@dataclass
class PaymentResult:
    status: str
    id: str
