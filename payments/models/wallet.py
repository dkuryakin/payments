import uuid

from sqlalchemy import Column, ForeignKey, DECIMAL, CHAR, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings import settings
from .base import BaseModel


class Wallet(BaseModel):
    __tablename__ = 'wallet'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)

    # use decimal against cumulative round errors
    amount = Column(
        DECIMAL(scale=settings.decimal_precision),
        CheckConstraint('amount >= 0'),
        nullable=False,
    )

    user_id = Column(UUID, ForeignKey('user.id'))
    currency_id = Column(CHAR(3), ForeignKey('currency.id'))

    user = relationship('User', back_populates="wallets")
    currency = relationship('Currency', back_populates="wallets")
    sent_transfers = relationship('TransfersHistory', back_populates='src_user')
    received_transfers = relationship('TransfersHistory', back_populates='dst_user')
