from src.domain.interfaces.repositories.transactions_repository import TransactionsRepository
from src.infrastructure.adapters.repositories.postgresql.models.transaction_model import TransactionModel
from src.domain.entities.transaction import Transaction


class PostgresSQLTransactionsRepository(TransactionsRepository):
    def __init__(self, session):
        self.session = session

    def save(self, transaction: Transaction):
        model = TransactionModel(**vars(transaction))
        self.session.add(model)
        self.session.commit()

    def get_by_id(self, transaction_id: str):
        model = self.session.query(TransactionModel).get(transaction_id)
        if model:
            return Transaction(**vars(model))
        return None

    def get_all(self):
        models = self.session.query(TransactionModel).all()
        return [Transaction(**vars(model)) for model in models]
