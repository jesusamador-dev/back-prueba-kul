import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    id: str = str(uuid.uuid4())
    amount: float
    currency: str
    customer_email: str
    customer_name: str
    status: str
    gateway_transaction_id: str = None
