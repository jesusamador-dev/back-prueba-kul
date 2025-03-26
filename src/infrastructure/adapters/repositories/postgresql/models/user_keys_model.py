from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserKeysModel(Base):
    __tablename__ = "user_keys"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    public_key_1 = Column(Text, nullable=False)
    private_key_1 = Column(Text, nullable=False)
    public_key_2 = Column(Text, nullable=False)
    private_key_2 = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
