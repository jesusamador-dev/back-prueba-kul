from src.domain.services.rsa_encryption_service import RSAEncryptionService
from src.domain.entities.transaction import Transaction


class TransactionEncryptor:
    def __init__(self, encryption_service: RSAEncryptionService):
        self.encryption_service = encryption_service

    def encrypt(self, transaction: Transaction) -> dict:
        return {
            "id": transaction.id,
            "amount": self.encryption_service.encrypt(str(transaction.amount)),
            "currency": self.encryption_service.encrypt(transaction.currency),
            "customer_name": self.encryption_service.encrypt(transaction.customer_name),
            "customer_email": self.encryption_service.encrypt(transaction.customer_email),
            "status": self.encryption_service.encrypt(transaction.status),
            "gateway_transaction_id": self.encryption_service.encrypt(transaction.gateway_transaction_id or ""),
            "date": transaction.created_at.strftime("%d/%m/%Y %H:%M")
        }
