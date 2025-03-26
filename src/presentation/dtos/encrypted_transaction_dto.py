from pydantic import BaseModel


class EncryptedTransactionDTO(BaseModel):
    amount: str
    currency: str
    customer_information: dict
    card_information: dict
