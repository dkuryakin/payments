from pydantic import BaseModel, UUID4

from validators import UsernameType


class UserView(BaseModel):
    id: UUID4
    username: UsernameType

    class Config:
        orm_mode = True
