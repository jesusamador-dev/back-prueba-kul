from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.application.use_cases.keys.generate_rsa_keys_use_case import GenerateRSAKeysUseCase
from src.domain.interfaces.repositories.user_keys_repository import UserKeysRepository
from src.infrastructure.adapters.repositories.postgresql.postgres_sql_user_keys_repository \
    import (PostgresSQLUserKeysRepository)
from src.infrastructure.adapters.repositories.postgresql.database_postgres import DatabasePostgres
from src.domain.services.rsa_key_generator_service import RSAKeyGeneratorService

router = APIRouter()


def get_db_session() -> Session:
    db = DatabasePostgres.get_instance()
    try:
        session = db.get_session()
        yield session
    finally:
        session.close()


def get_user_keys_repository(db: Session = Depends(get_db_session)) -> UserKeysRepository:
    return PostgresSQLUserKeysRepository(session=db)


@router.post("/keys/rsa/{user_id}")
def generate_rsa_keys(user_id: str,
                      repo: UserKeysRepository = Depends(get_user_keys_repository)):
    service = RSAKeyGeneratorService()
    use_case = GenerateRSAKeysUseCase(service, repo)
    return use_case.execute(user_id=user_id)


@router.get("/keys/rsa/{user_id}")
def get_rsa_keys(user_id: str,
                 response: Response,
                 repo: UserKeysRepository = Depends(get_user_keys_repository)):
    result = repo.get_by_user_id(user_id)
    if not result:
        return {"message": "No keys found for this user."}
    response.set_cookie(
        key="user-keys",
        value=user_id,
        httponly=True,
        samesite="Lax",
        secure=True
    )
    return {
        "public_key": result.public_key_1,
        "private_key": result.private_key_2
    }
