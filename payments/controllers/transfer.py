from typing import List

from fastapi import Depends, Form, Query
from pydantic import UUID4
from sqlalchemy import or_

from models.base import db
from models.transfer import Transfer
from models.user import User
from models.wallet import Wallet
from utils.transfer import (
    check_user_own_wallet, check_same_wallet, check_both_amounts, check_enough_amount, get_exchange_rate,
    get_transfer_fee, fix_amounts,
)
from utils.user import get_me
from validators import TransferAmountType, MessageType, CurrencyType, SortType


async def transfer_create(
        src_wallet: UUID4 = Form(...),
        dst_wallet: UUID4 = Form(...),
        src_amount: TransferAmountType = Form(None),
        dst_amount: TransferAmountType = Form(None),
        message: MessageType = Form(None),
        user: User = Depends(get_me),
) -> Transfer:
    check_same_wallet(src_wallet, dst_wallet)
    check_both_amounts(src_amount, dst_amount)
    async with db.transaction() as tx:
        src_wallet = await Wallet.query.where(Wallet.id == src_wallet).with_for_update().gino.first()
        check_user_own_wallet(user, src_wallet)

        dst_wallet = await Wallet.query.where(Wallet.id == dst_wallet).with_for_update().gino.first()

        transfer_fee = await get_transfer_fee(src_wallet, dst_wallet)
        exchange_rate = await get_exchange_rate(src_wallet, dst_wallet)

        src_amount, dst_amount = fix_amounts(src_amount, dst_amount, transfer_fee, exchange_rate)

        check_enough_amount(src_wallet, src_amount)

        await Wallet.update.values(amount=Wallet.amount - src_amount).where(Wallet.id == src_wallet.id).gino.status()
        await Wallet.update.values(amount=Wallet.amount + dst_amount).where(Wallet.id == dst_wallet.id).gino.status()

        transfer = await Transfer.create(
            message=message,
            src_amount=src_amount,
            dst_amount=dst_amount,
            src_user_id=src_wallet.user_id,
            src_wallet_id=src_wallet.id,
            src_currency_id=src_wallet.currency_id,
            dst_user_id=dst_wallet.user_id,
            dst_wallet_id=dst_wallet.id,
            dst_currency_id=dst_wallet.currency_id,
        )
        return transfer


async def transfer_list(
        src_currency: CurrencyType = Query(None),
        dst_currency: CurrencyType = Query(None),
        src_amount_lt: TransferAmountType = Query(None),
        src_amount_gt: TransferAmountType = Query(None),
        dst_amount_lt: TransferAmountType = Query(None),
        dst_amount_gt: TransferAmountType = Query(None),
        src_wallet: UUID4 = Query(None),
        dst_wallet: UUID4 = Query(None),
        sort_created_at: SortType = Query(SortType.desc),
        user: User = Depends(get_me),
) -> List[Transfer]:
    transfers = Transfer.query.where(or_(
        Transfer.src_user_id == user.id,
        Transfer.dst_user_id == user.id,
    ))

    if src_currency is not None:
        transfers = transfers.where(Transfer.src_currency_id == src_currency)
    if dst_currency is not None:
        transfers = transfers.where(Transfer.dst_currency_id == dst_currency)
    if src_amount_lt is not None:
        transfers = transfers.where(Transfer.src_amount < src_amount_lt)
    if src_amount_gt is not None:
        transfers = transfers.where(Transfer.src_amount > src_amount_gt)
    if dst_amount_lt is not None:
        transfers = transfers.where(Transfer.dst_amount < dst_amount_lt)
    if dst_amount_gt is not None:
        transfers = transfers.where(Transfer.dst_amount > dst_amount_gt)
    if src_wallet is not None:
        transfers = transfers.where(Transfer.src_wallet_id == src_wallet)
    if dst_wallet is not None:
        transfers = transfers.where(Transfer.dst_wallet_id == dst_wallet)

    if sort_created_at is not None:
        if sort_created_at == SortType.asc:
            direction = Transfer.created_at.asc()
        else:
            direction = Transfer.created_at.desc()
        transfers = transfers.order_by(direction)

    return await transfers.gino.all()
