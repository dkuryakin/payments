from asyncpg.exceptions import UniqueViolationError
from fastapi import Depends, HTTPException, Form

from models.base import db
from models.user import User
from utils.token import get_password_hash
from utils.user import create_default_wallets, get_me
from validators import UsernameType, PasswordType


async def user_create(
        username: UsernameType = Form(...),
        password: PasswordType = Form(...),
) -> User:
    try:
        async with db.transaction():
            user = await User.create(
                username=username,
                hashed_password=get_password_hash(password),
            )
            await create_default_wallets(user)
            return user
    except UniqueViolationError:
        raise HTTPException(
            status_code=409,
            detail='Duplicate username',
        )


async def user_get(user: User = Depends(get_me)) -> User:
    return user
