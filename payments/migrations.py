from models.base import db


async def migrations():
    # Just create all the tables. Dummy initial migration.
    await db.gino.create_all()
