from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.transaction import Transaction


class TransactionsRepository(ABC):

    @abstractmethod
    def save(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Transaction]:
        raise NotImplementedError
