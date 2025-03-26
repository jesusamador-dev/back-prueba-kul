from src.domain.entities.user_keys import UserKeys
from src.domain.interfaces.repositories.user_keys_repository import UserKeysRepository
from src.domain.services.rsa_key_generator_service import RSAKeyGeneratorService


class GenerateRSAKeysUseCase:
    def __init__(self, rsa_generator: RSAKeyGeneratorService, repository: UserKeysRepository):
        self.rsa_generator = rsa_generator
        self.repository = repository

    def execute(self, user_id: str) -> dict:
        keys_pair_1 = self.rsa_generator.generate_key_pair()
        keys_pair_2 = self.rsa_generator.generate_key_pair()

        user_key = UserKeys(
            user_id=user_id,
            public_key_1=keys_pair_1.public_key,
            private_key_1=keys_pair_1.private_key,
            public_key_2=keys_pair_2.public_key,
            private_key_2=keys_pair_2.private_key,
        )

        self.repository.save(user_key)

        return {
            "public_key_1": user_key.public_key_1,
            "private_key_2": user_key.private_key_2,
        }
