from abc import ABC, abstractmethod
from src.domain.entities.user_keys import UserKeys
from typing import Optional


class UserKeysRepository(ABC):

    @abstractmethod
    def save(self, user_keys: UserKeys) -> None:
        """Guarda los pares de llaves RSA de un usuario."""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[UserKeys]:
        """Recupera los pares de llaves por user_id, si existen."""
        pass
