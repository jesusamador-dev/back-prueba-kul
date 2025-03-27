from src.domain.services.rsa_encryption_service import RSAEncryptionService
from src.presentation.dtos.transaction_dto import CreateTransactionDTO
from src.presentation.dtos.encrypted_transaction_dto import EncryptedTransactionDTO


class TransactionDecryptor:
    def __init__(self, encryption_service: RSAEncryptionService):
        self.encryption_service = encryption_service

    def decrypt(self, encrypted_dto: EncryptedTransactionDTO) -> CreateTransactionDTO:
        decrypted_data = {
            "amount": self.encryption_service.decrypt(encrypted_dto.amount),
            "currency": self.encryption_service.decrypt(encrypted_dto.currency),
            "customer_information": {
                k: self.encryption_service.decrypt(v)
                for k, v in encrypted_dto.customer_information.items()
                if v != ""
            },
            "card_information": {
                k: self.encryption_service.decrypt(v)
                for k, v in encrypted_dto.card_information.items()
                if v != ""
            },
        }

        return CreateTransactionDTO(**decrypted_data)