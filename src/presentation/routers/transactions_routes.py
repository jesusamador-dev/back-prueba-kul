from fastapi import APIRouter, Request, Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from src.application.use_cases.transactions.create_transaction_use_case import CreateTransactionUseCase
from src.application.use_cases.transactions.get_all_transactions import GetAllTransactionsUseCase
from src.application.use_cases.transactions.get_transaction import GetTransactionByIdUseCase
from src.domain.interfaces.gateways.payment_gateway import PaymentGateway
from src.domain.interfaces.repositories.transactions_repository import TransactionsRepository
from src.domain.interfaces.repositories.user_keys_repository import UserKeysRepository
from src.infrastructure.adapters.gateways.blumonpay_payment_gateway import BlumonpayPaymentGateway
from src.infrastructure.adapters.repositories.postgresql.database_postgres import DatabasePostgres
from src.infrastructure.adapters.repositories.postgresql.postgres_sql_transactions_repository import \
    PostgresSQLTransactionsRepository
from src.presentation.dtos.transaction_dto import CreateTransactionDTO, TransactionResponseDTO
from src.presentation.mappers.transaction_request_mapper import TransactionRequestMapper
from src.presentation.mappers.transaction_response_encrypt_mapper import TransactionResponseEncryptMapper
from src.presentation.routers.keys_routes import get_user_keys_repository

router = APIRouter()


def get_payment_gateway() -> PaymentGateway:
    return BlumonpayPaymentGateway()


def get_db_session() -> Session:
    db = DatabasePostgres.get_instance()
    try:
        session = db.get_session()
        yield session
    finally:
        session.close()


def get_transaction_repository(db: Session = Depends(get_db_session)) -> TransactionsRepository:
    return PostgresSQLTransactionsRepository(session=db)


def get_transaction_request_mapper(
    repo: UserKeysRepository = Depends(get_user_keys_repository),
) -> TransactionRequestMapper:
    return TransactionRequestMapper(user_keys_repo=repo)


def get_transaction_response_mapper(
    repo: UserKeysRepository = Depends(get_user_keys_repository),
) -> TransactionResponseEncryptMapper:
    return TransactionResponseEncryptMapper(user_keys_repo=repo)


@router.post("/transactions")
def create_transaction(
    transaction: CreateTransactionDTO = Depends(get_transaction_request_mapper),
    payment_gateway: PaymentGateway = Depends(get_payment_gateway),
    transactions_repo: TransactionsRepository = Depends(get_transaction_repository)
):
    use_case = CreateTransactionUseCase(payment_gateway, transactions_repo)
    return use_case.execute(transaction_data=transaction)


@router.get("/transactions")
def get_all_transactions(
    request: Request,
    user_id: str = Cookie(None, alias="user-keys"),
    repo: TransactionsRepository = Depends(get_transaction_repository),
    encrypt_mapper: TransactionResponseEncryptMapper = Depends(get_transaction_response_mapper)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user-keys cookie")

    use_case = GetAllTransactionsUseCase(repo)
    transactions = use_case.execute()
    return encrypt_mapper.encrypt_many(transactions, user_id)


@router.get("/transactions/{transaction_id}")
def get_transaction_by_id(
    transaction_id: str,
    request: Request,
    user_id: str = Cookie(None, alias="user-keys"),
    repo: TransactionsRepository = Depends(get_transaction_repository),
    encrypt_mapper: TransactionResponseEncryptMapper = Depends(get_transaction_response_mapper)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user-keys cookie")

    use_case = GetTransactionByIdUseCase(repo)
    transaction = use_case.execute(transaction_id)
    return encrypt_mapper.encrypt_one(transaction, user_id)

