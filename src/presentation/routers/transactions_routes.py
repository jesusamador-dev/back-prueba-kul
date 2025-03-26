from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List
from src.application.use_cases.create_transaction_use_case import CreateTransactionUseCase
from src.domain.interfaces.gateways.payment_gateway import PaymentGateway
from src.infrastructure.adapters.gateways.blumonpay_payment_gateway import BlumonpayPaymentGateway
from src.presentation.dtos.transaction_dto import CreateTransactionDTO

router = APIRouter()


def get_payment_gateway():
    return BlumonpayPaymentGateway()


@router.post("/transactions")
def create_transaction(transaction: CreateTransactionDTO,
                       payment_gateway: PaymentGateway = Depends(get_payment_gateway)):
    use_case = CreateTransactionUseCase(payment_gateway)
    return use_case.execute(transaction_data=transaction)

