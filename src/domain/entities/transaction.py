import uuid
from dataclasses import dataclass

from src.domain.config.constants import CURRENCY_ISO_TO_CODE


@dataclass
class Transaction:
    amount: float
    currency: str
    customer_email: str
    customer_name: str
    status: str
    gateway_transaction_id: str = None
    id: str = str(uuid.uuid4())

    def convert_currency_iso_to_code(self) -> str:
        return CURRENCY_ISO_TO_CODE.get(self.currency)
