from typing import Optional
from sqlmodel import SQLModel
from schemas.attribute import AttributeRead
from schemas.product import ProductDefault

class VariantDefault(SQLModel):
    price: int
    stock: int


class VariantCreate(VariantDefault):
    product_id: int
    attribute_ids: Optional[list[int]] = None


class VariantUpdate(SQLModel):
    price: Optional[int] = None
    stock: Optional[int] = None
    product_id: Optional[int] = None
    attribute_ids: Optional[list[int]] = None


class VariantRead(VariantDefault):
    id: int
    product_id: int
    product: ProductDefault
    attributes: list[AttributeRead] = []
