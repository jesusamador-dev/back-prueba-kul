from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TransactionModel(Base):
    __tablename__ = 'transactions'
    model_config = ConfigDict(from_attributes=True)

    id = Column(UUID(as_uuid=True), primary_key=True)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(3), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_name = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)
    gateway_transaction_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
