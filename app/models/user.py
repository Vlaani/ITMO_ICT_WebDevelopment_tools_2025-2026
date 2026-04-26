from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.order import Order

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str = Field(index=True, unique=True)
    username: str
    email: str = Field(index=True, unique=True)
    password: str
    orders: list["Order"] = Relationship(back_populates="user")
