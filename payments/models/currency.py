from sqlalchemy import Column, CHAR, Float, CheckConstraint
from sqlalchemy.orm import relationship

from settings import settings
from .base import BaseModel


class Currency(BaseModel):
    __tablename__ = 'currency'

    # currency code, u.s. dollar = usd
    id = Column(CHAR(3), primary_key=True)

    # suppose we have simple transfer fee mechanics (cross-user transfers):
    # received_amount = (1 - transfer_fee) * sent_amount
    transfer_fee = Column(
        Float,
        CheckConstraint('0 <= transfer_fee AND transfer_fee < 1'),
        nullable=False,
        default=settings.default_transfer_fee,
    )

    wallets = relationship('Wallet', back_populates="currency")