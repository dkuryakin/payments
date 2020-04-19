import datetime
import uuid

from sqlalchemy import Column, ForeignKey, CHAR, DECIMAL, String, CheckConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings import settings
from .base import BaseModel


class Transfer(BaseModel):
    __tablename__ = 'transfer'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    message = Column(String(length=128), nullable=True)
    src_amount = Column(
        DECIMAL(scale=settings.decimal_precision),
        CheckConstraint('src_amount > 0'),
        nullable=False,
    )
    dst_amount = Column(
        DECIMAL(scale=settings.decimal_precision),
        CheckConstraint('dst_amount > 0'),
        nullable=False,
    )

    # There are some intentional redundancy (performance related purposes).

    src_user_id = Column(UUID, ForeignKey('user.id'))
    src_wallet_id = Column(UUID, ForeignKey('wallet.id'))
    src_currency_id = Column(CHAR(3), ForeignKey('currency.id'))

    dst_user_id = Column(UUID, ForeignKey('user.id'))
    dst_wallet_id = Column(UUID, ForeignKey('wallet.id'))
    dst_currency_id = Column(CHAR(3), ForeignKey('currency.id'))

    src_user = relationship('User', back_populates='sent_transfers')
    src_wallet = relationship('Wallet', back_populates='sent_transfers')
    src_currency = relationship('Currency')

    dst_user = relationship('User', back_populates='received_transfers')
    dst_wallet = relationship('Wallet', back_populates='received_transfers')
    dst_currency = relationship('Currency')
