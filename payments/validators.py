from enum import Enum

from pydantic import condecimal, constr

from settings import settings

UsernameType = constr(
    strip_whitespace=True,
    min_length=3,
    max_length=128,
    regex=r'^[a-zA-Z0-9_]+$',
)

PasswordType = constr(
    min_length=3,
    max_length=128,
)

TransferAmountType = condecimal(
    gt=0,
    decimal_places=settings.decimal_precision,
)

BalanceAmountType = condecimal(
    ge=0,
    decimal_places=settings.decimal_precision,
)

NameType = constr(
    strip_whitespace=True,
    max_length=128,
)

MessageType = constr(
    strip_whitespace=True,
    max_length=128,
)

CurrencyType = constr(min_length=3, max_length=3)


class SortType(str, Enum):
    asc = 'asc'
    desc = 'desc'
