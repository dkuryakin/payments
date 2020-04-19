import uuid

from sqlalchemy import Column, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    # It's better to use UUID insted of serial for some reasons.
    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    # For test task I don't implement email, active, disabled, created_at,
    # and other fields required for production.
    username = Column(String(128), unique=True, index=True, nullable=False)

    hashed_password = Column(Text, nullable=False)

    wallets = relationship('Wallet', back_populates="user")
    sent_transfers = relationship('TransfersHistory', back_populates='src_user')
    received_transfers = relationship('TransfersHistory', back_populates='dst_user')
