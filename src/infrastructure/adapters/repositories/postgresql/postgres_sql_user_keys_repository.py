from src.domain.interfaces.repositories.user_keys_repository import UserKeysRepository
from src.domain.entities.user_keys import UserKeys
from src.infrastructure.adapters.repositories.postgresql.models.user_keys_model import UserKeysModel


class PostgresSQLUserKeysRepository(UserKeysRepository):
    def __init__(self, session):
        self.session = session

    def save(self, user_keys: UserKeys) -> None:
        model = UserKeysModel(**vars(user_keys))
        self.session.merge(model)
        self.session.commit()

    def get_by_user_id(self, user_id: str) -> UserKeys | None:
        model = self.session.query(UserKeysModel).filter_by(user_id=user_id).first()
        if model:
            return UserKeys(
                id=model.id,
                user_id=model.user_id,
                public_key_1=model.public_key_1,
                private_key_1=model.private_key_1,
                public_key_2=model.public_key_2,
                private_key_2=model.private_key_2,
                created_at=model.created_at
            )
        return None
