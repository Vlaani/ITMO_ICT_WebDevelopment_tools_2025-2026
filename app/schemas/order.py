from datetime import datetime

from sqlmodel import SQLModel
from schemas.variant import VariantRead
from models.order import OrderStatus

class OrderVariantItemCreate(SQLModel):
    variant_id: int
    quantity: int


class OrderCreate(SQLModel):
    items: list[OrderVariantItemCreate]


class OrderVariantItemRead(SQLModel):
    variant: VariantRead
    quantity: int


class OrderRead(SQLModel):
    id: int
    created_at: datetime
    status: OrderStatus
    total_price: int
    items: list[OrderVariantItemRead]
