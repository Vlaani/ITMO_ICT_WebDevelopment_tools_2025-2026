from typing import Optional
from sqlmodel import SQLModel
from schemas.attribute import AttributeRead


class ProductDefault(SQLModel):
    name: str = ""
    description: Optional[str] = ""


class ProductCreate(SQLModel):
    name: str = ""
    description: Optional[str] = ""
    attribute_ids: Optional[list[int]] = None


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    attribute_ids: Optional[list[int]] = None


class ProductVariant(SQLModel):
    id: int
    price: int
    stock: int
    attributes: list[AttributeRead] = []


class ProductRead(ProductDefault):
    id: int
    attributes: list[AttributeRead] = []
    variants: list[ProductVariant] = []
