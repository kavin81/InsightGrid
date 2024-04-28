from datetime import date
from typing import Optional

from pydantic import EmailStr
from redis_om import Field, HashModel, Migrator


class UserData(HashModel):

    username: str = Field(index=True)
    email: EmailStr = Field(index=True)
    password: str = Field(index=True)

    join_date: date
    last_login: date

    is_editor: Optional[bool] = False  # can edit posts
    is_mod: Optional[bool] = False  # can ban users
    is_god: Optional[bool] = False  # can do anything


Migrator().run()
