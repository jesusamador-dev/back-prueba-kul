from fastapi import Request, HTTPException, status
from src.domain.interfaces.repositories.user_keys_repository import UserKeysRepository
from src.application.services.transaction_decryptor import TransactionDecryptor
from src.domain.services.rsa_encryption_service import RSAEncryptionService
from src.presentation.dtos.transaction_dto import CreateTransactionDTO
from src.presentation.dtos.encrypted_transaction_dto import EncryptedTransactionDTO


class TransactionRequestMapper:
    def __init__(self, user_keys_repo: UserKeysRepository):
        self.user_keys_repo = user_keys_repo

    async def __call__(self, request: Request) -> CreateTransactionDTO:
        user_id = request.cookies.get("user-keys")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing user-keys cookie")

        user_keys = self.user_keys_repo.get_by_user_id(user_id)
        if not user_keys:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Keys not found for this user")

        encryption_service = RSAEncryptionService(
            private_key_pem=user_keys.private_key_1,
            public_key_pem=user_keys.public_key_2
        )

        decryptor = TransactionDecryptor(encryption_service)

        body = await request.json()
        encrypted_dto = EncryptedTransactionDTO(**body)

        return decryptor.decrypt(encrypted_dto)
