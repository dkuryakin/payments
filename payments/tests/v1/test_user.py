from decimal import Decimal

import pytest
from aiohttp.client import ClientSession
from sqlalchemy import and_

from models.base import db
from models.user import User
from models.wallet import Wallet
from settings import settings
from utils.token import verify_password
from .base import api_url


@pytest.mark.asyncio
async def test_user_create():
    async with db.with_bind(settings.postgres_dsn):
        data = dict(username='user1', password='password1')
        async with ClientSession()as sess:
            user = await sess.post(api_url + '/user', data=data)
            user = await user.json()
            assert 'user1' == user.get('username')

            user = await User.query.where(User.id == user['id']).gino.first()
            assert 'user1' == user.username

            assert verify_password('password1', user.hashed_password)

            usd: Wallet = await Wallet.query.where(and_(
                Wallet.user_id == user.id,
                Wallet.currency_id == 'USD',
            )).gino.first()
            assert usd
            assert usd.amount == Decimal('100')

            eur: Wallet = await Wallet.query.where(and_(
                Wallet.user_id == user.id,
                Wallet.currency_id == 'EUR',
            )).gino.first()
            assert eur
            assert eur.amount == Decimal('0')

            cny: Wallet = await Wallet.query.where(and_(
                Wallet.user_id == user.id,
                Wallet.currency_id == 'CNY',
            )).gino.first()
            assert cny
            assert cny.amount == Decimal('0')
