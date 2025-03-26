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

    def get_by_id(self, id: str):
        model = self.session.query(TransactionModel).get(id)
        if model:
            return Transaction(
                id=model.id,
                amount=float(model.amount),
                currency=model.currency,
                customer_email=model.customer_email,
                customer_name=model.customer_name,
                status=model.status,
                gateway_transaction_id=model.gateway_transaction_id,
                created_at=model.created_at
            )
        return None

    def get_all(self):
        models = self.session.query(TransactionModel).all()
        return [
            Transaction(
                id=model.id,
                amount=float(model.amount),
                currency=model.currency,
                customer_email=model.customer_email,
                customer_name=model.customer_name,
                status=model.status,
                gateway_transaction_id=model.gateway_transaction_id,
                created_at=model.created_at
            )
            for model in models
        ]
