import uuid

from sqlalchemy import Column, Float, ForeignKey, UniqueConstraint, CHAR, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel


class Exchange(BaseModel):
    __tablename__ = 'exchange'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    # dst_currency_amount = rate * src_currency_amount
    rate = Column(Float, CheckConstraint('rate > 0'), nullable=False)

    src_currency_id = Column(CHAR(3), ForeignKey('currency.id'))
    dst_currency_id = Column(CHAR(3), ForeignKey('currency.id'))

    src_currency = relationship('Currency')
    dst_currency = relationship('Currency')

    __table_args__ = (
        UniqueConstraint('src_currency_id', 'dst_currency_id', name='uniq_src_dst_currencies'),
    )
