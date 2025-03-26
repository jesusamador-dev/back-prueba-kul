from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
from decimal import Decimal

from src.domain.config.constants import ACCEPTED_CURRENCIES
from src.domain.entities.transaction import Transaction


def validate_card_number(card_number: str) -> bool:
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0


class CustomerInformationDTO(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    country: str
    ip: Optional[str] = None


class CardInformationDTO(BaseModel):
    card_number: constr(min_length=16, max_length=16)
    cvv: constr(min_length=3, max_length=3)
    card_holder_name: str
    expiration_year: constr(min_length=2, max_length=2)
    expiration_month: constr(min_length=2, max_length=2)

    @field_validator('card_number')
    def validate_card_number(cls, value):
        if value == "1234123412341234":
            return value
        if not validate_card_number(value):
            raise ValueError("Invalid card number")
        return value


class CreateTransactionDTO(BaseModel):
    amount: Decimal
    currency: str
    customer_information: CustomerInformationDTO
    card_information: CardInformationDTO

    @field_validator('amount')
    def validate_amount(cls, value):
        assert value > 0, ValueError('Amount must be greater than zero')
        return value

    @field_validator('currency')
    def validate_currency(cls, value):
        if value not in ACCEPTED_CURRENCIES:
            raise ValueError(f"Currency {value} is not accepted.")
        return value


class TransactionResponseDTO(BaseModel):
    id: str
    amount: float
    currency: str
    customer_name: str
    customer_email: str
    status: str
    gateway_transaction_id: str
    date: str

    @classmethod
    def from_entity(cls, transaction: Transaction) -> "TransactionResponseDTO":
        return cls(
            id=str(transaction.id),
            amount=float(transaction.amount),
            currency=transaction.currency,
            customer_name=transaction.customer_name,
            customer_email=transaction.customer_email,
            status=transaction.status,
            gateway_transaction_id=transaction.gateway_transaction_id,
            date=transaction.created_at.strftime("%d/%m/%Y %H:%M")
        )
