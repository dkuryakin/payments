from typing import List

from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

from models.currency import Currency
from models.user import User
from models.wallet import Wallet
from settings import settings
from .token import get_username_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.token_url)


async def create_default_wallets(user: User) -> List[Wallet]:
    usd = await Currency.get('USD')
    cny = await Currency.get('CNY')
    eur = await Currency.get('EUR')
    usd = await Wallet.create(name='Default USD Wallet', amount=100, user_id=user.id, currency_id=usd.id)
    cny = await Wallet.create(name='Default CNY Wallet', amount=0, user_id=user.id, currency_id=cny.id)
    eur = await Wallet.create(name='Default EUR Wallet', amount=0, user_id=user.id, currency_id=eur.id)
    return [usd, cny, eur]


async def get_me(token: str = Security(oauth2_scheme)) -> User:
    error = HTTPException(
        status_code=401,
        detail="Invalid token",
    )
    username = get_username_from_token(token)
    if username is None:
        raise error
    user = await User.query.where(User.username == username).gino.first()
    if user is None:
        raise user
    return user
