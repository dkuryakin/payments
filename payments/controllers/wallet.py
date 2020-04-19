from typing import List

from fastapi import Depends

from models.user import User
from models.wallet import Wallet
from utils.user import get_me


async def wallet_list(user: User = Depends(get_me)) -> List[Wallet]:
    return await Wallet.query.where(Wallet.user_id == user.id).gino.all()
