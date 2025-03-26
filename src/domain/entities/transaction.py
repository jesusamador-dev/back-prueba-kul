import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    amount: float
    currency: str
    customer_email: str
    customer_name: str
    status: str
    gateway_transaction_id: str = None
    id: str = str(uuid.uuid4())
