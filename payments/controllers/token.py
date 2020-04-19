from fastapi import HTTPException, Form

from models.user import User
from settings import settings
from utils.token import verify_password, create_token
from validators import UsernameType, PasswordType
from views.token import TokenView


async def token_create(
        username: UsernameType = Form(...),
        password: PasswordType = Form(...),
) -> TokenView:
    user = await User.query.where(User.username == username).gino.first()
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=403,
            detail='Wrong user or password',
        )
    return TokenView(
        access_token=create_token(username, settings.jwt_lifetime_seconds),
        token_type='bearer',
    )
