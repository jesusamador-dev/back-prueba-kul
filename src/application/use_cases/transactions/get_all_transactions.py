from src.domain.interfaces.repositories.transactions_repository import TransactionsRepository
from src.domain.entities.transaction import Transaction
from typing import List


class GetAllTransactionsUseCase:
    def __init__(self, transactions_repository: TransactionsRepository):
        self.transactions_repository = transactions_repository

    def execute(self) -> List[Transaction]:
        """
        Retorna todas las transacciones almacenadas.
        """
        return self.transactions_repository.get_all()
