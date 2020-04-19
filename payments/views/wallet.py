from pydantic import BaseModel, UUID4

from validators import BalanceAmountType, CurrencyType, NameType


class WalletView(BaseModel):
    id: UUID4
    name: NameType
    currency_id: CurrencyType
    amount: BalanceAmountType

    class Config:
        orm_mode = True
