from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

if TYPE_CHECKING:
    from models.user import User
    from models.variant import Variant


class OrderStatus(Enum):
    created = "created"
    canceled = "canceled"
    shipped = "shipped"


class OrderVariantLink(SQLModel, table=True):
    order_id: int = Field(default=None, foreign_key="order.id", primary_key=True)
    variant_id: int = Field(default=None, foreign_key="variant.id", primary_key=True)
    variant: "Variant" = Relationship()
    quantity: int = Field(default=1, ge=1)


class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: OrderStatus = Field(default=OrderStatus.created, index=True)
    total_price: int = Field(default=0, ge=0)

    user: "User" = Relationship(back_populates="orders")
    variants: List["Variant"] = Relationship(back_populates="orders", link_model=OrderVariantLink)
    items: List[OrderVariantLink] = Relationship() 
