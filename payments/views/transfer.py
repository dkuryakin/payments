from typing import Optional

from pydantic import BaseModel, UUID4

from validators import TransferAmountType, MessageType, CurrencyType


class TransferView(BaseModel):
    id: UUID4
    message: Optional[MessageType]
    src_amount: TransferAmountType
    dst_amount: TransferAmountType

    src_user_id: UUID4
    src_wallet_id: UUID4
    src_currency_id: CurrencyType

    dst_user_id: UUID4
    dst_wallet_id: UUID4
    dst_currency_id: CurrencyType

    class Config:
        orm_mode = True
