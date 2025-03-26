from src.domain.interfaces.repositories.transactions_repository import TransactionsRepository
from src.domain.entities.transaction import Transaction
from fastapi import HTTPException


class GetTransactionByIdUseCase:
    def __init__(self, transactions_repository: TransactionsRepository):
        self.transactions_repository = transactions_repository

    def execute(self, transaction_id: str) -> Transaction:
        transaction = self.transactions_repository.get_by_id(transaction_id)

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return transaction
