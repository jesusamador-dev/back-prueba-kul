from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List
from sqlalchemy.orm import Session

from src.application.use_cases.create_transaction_use_case import CreateTransactionUseCase
from src.domain.interfaces.gateways.payment_gateway import PaymentGateway
from src.domain.interfaces.repositories.transactions_repository import TransactionsRepository
from src.infrastructure.adapters.gateways.blumonpay_payment_gateway import BlumonpayPaymentGateway
from src.infrastructure.adapters.repositories.postgresql.database_postgres import DatabasePostgres
from src.infrastructure.adapters.repositories.postgresql.postgres_sql_transactions_repository import \
    PostgresSQLTransactionsRepository
from src.presentation.dtos.transaction_dto import CreateTransactionDTO

router = APIRouter()


def get_payment_gateway() -> PaymentGateway:
    return BlumonpayPaymentGateway()


# Define una función para obtener una sesión de base de datos
def get_db_session() -> Session:
    db = DatabasePostgres.get_instance()
    try:
        session = db.get_session()
        yield session
    finally:
        session.close()


# Ahora usa esta función para inyectar la sesión de base de datos en tu repositorio
def get_transaction_repository(db: Session = Depends(get_db_session)) -> TransactionsRepository:
    return PostgresSQLTransactionsRepository(session=db)


@router.post("/transactions")
def create_transaction(transaction: CreateTransactionDTO,
                       payment_gateway: PaymentGateway = Depends(get_payment_gateway),
                       transactions_repo: TransactionsRepository = Depends(get_transaction_repository)):
    use_case = CreateTransactionUseCase(payment_gateway, transactions_repo)
    return use_case.execute(transaction_data=transaction)

