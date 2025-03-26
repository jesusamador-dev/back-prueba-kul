from fastapi import Request, HTTPException, status
from src.domain.interfaces.repositories.user_keys_repository import UserKeysRepository
from src.domain.services.rsa_encryption_service import RSAEncryptionService
from src.application.services.transaction_encryptor import TransactionEncryptor
from src.domain.entities.transaction import Transaction


class TransactionResponseEncryptMapper:
    def __init__(self, user_keys_repo: UserKeysRepository):
        self.user_keys_repo = user_keys_repo

    def get_encryptor(self, user_id: str) -> TransactionEncryptor:
        user_keys = self.user_keys_repo.get_by_user_id(user_id)
        if not user_keys:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Keys not found for this user")

        encryption_service = RSAEncryptionService(
            private_key_pem=user_keys.private_key_1,
            public_key_pem=user_keys.public_key_2
        )

        return TransactionEncryptor(encryption_service)

    def encrypt_one(self, transaction: Transaction, user_id: str) -> dict:
        encryptor = self.get_encryptor(user_id)
        return encryptor.encrypt(transaction)

    def encrypt_many(self, transactions: list[Transaction], user_id: str) -> list[dict]:
        encryptor = self.get_encryptor(user_id)
        return [encryptor.encrypt(tx) for tx in transactions]
