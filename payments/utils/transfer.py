from decimal import Decimal
from typing import Tuple

from fastapi import HTTPException
from sqlalchemy import and_

from models.currency import Currency
from models.exchange import Exchange
from models.user import User
from models.wallet import Wallet
from utils.common import quantize
from validators import TransferAmountType


def check_same_wallet(src_wallet: Wallet, dst_wallet: Wallet):
    if src_wallet == dst_wallet:
        raise HTTPException(
            status_code=400,
            detail='Unable to transfer money to the same wallet',
        )


def check_both_amounts(src_amount: TransferAmountType, dst_amount: TransferAmountType):
    if (src_amount is None) == (dst_amount is None):
        raise HTTPException(
            status_code=400,
            detail='Specify one of src_amount/dst_amount',
        )


def check_user_own_wallet(user: User, wallet: Wallet):
    if wallet.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail='Unable to transfer from source wallet',
        )


async def get_transfer_fee(src_wallet: Wallet, dst_wallet: Wallet) -> float:
    if src_wallet.user_id == dst_wallet.user_id:
        return 0
    src_currency = await Currency.get(src_wallet.currency_id)
    return src_currency.transfer_fee


async def get_exchange_rate(src_wallet: Wallet, dst_wallet: Wallet) -> float:
    if src_wallet.currency_id == dst_wallet.currency_id:
        return 1
    exchange = await Exchange.query.where(and_(
        Exchange.src_currency_id == src_wallet.currency_id,
        Exchange.dst_currency_id == dst_wallet.currency_id,
    )).gino.first()
    return exchange.rate


def fix_amounts(
        src_amount: TransferAmountType,
        dst_amount: TransferAmountType,
        transfer_fee: float,
        exchange_rate: float,
) -> Tuple[TransferAmountType, TransferAmountType]:
    if src_amount is None:
        src_amount = float(dst_amount) / (1 - transfer_fee) / exchange_rate
        src_amount = Decimal.from_float(src_amount)

    src_amount = quantize(src_amount)

    dst_amount = float(src_amount) * (1 - transfer_fee) * exchange_rate
    dst_amount = quantize(Decimal.from_float(dst_amount))

    return src_amount, dst_amount


def check_enough_amount(wallet: Wallet, amount: TransferAmountType):
    if wallet.amount < amount:
        extra = amount - wallet.amount
        raise HTTPException(
            status_code=400,
            detail=f'Need extra money on source wallet ({extra} more)',
        )
