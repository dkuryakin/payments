from asyncpg.exceptions import UniqueViolationError

from models.base import db
from models.currency import Currency
from models.exchange import Exchange


async def fixtures():
    # Fill currencies. Move to real fixtures in production.
    try:
        async with db.transaction():
            usd = await Currency.create(id='USD')
            cny = await Currency.create(id='CNY')
            eur = await Currency.create(id='EUR')

            await Exchange.create(src_currency_id=cny.id, dst_currency_id=usd.id, rate=7)
            await Exchange.create(src_currency_id=usd.id, dst_currency_id=cny.id, rate=0.14)

            await Exchange.create(src_currency_id=cny.id, dst_currency_id=eur.id, rate=7.7)
            await Exchange.create(src_currency_id=eur.id, dst_currency_id=cny.id, rate=0.12)

            await Exchange.create(src_currency_id=usd.id, dst_currency_id=eur.id, rate=1.1)
            await Exchange.create(src_currency_id=eur.id, dst_currency_id=usd.id, rate=0.9)
    except UniqueViolationError:
        pass
