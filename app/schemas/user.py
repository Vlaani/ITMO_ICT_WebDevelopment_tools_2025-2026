from typing import Optional
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel
from pydantic import BaseModel
from schemas.order import OrderRead
from models.order import Order

if TYPE_CHECKING:
    from models.order import Order

class UserBase(SQLModel):
    login: str
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(SQLModel):
    login: str
    password: str


class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class UserRead(UserBase):
    id: int

class UserReadFull(UserRead):
    orders: list[Order] = []

class Token(BaseModel):
    access_token: str
    token_type: str
