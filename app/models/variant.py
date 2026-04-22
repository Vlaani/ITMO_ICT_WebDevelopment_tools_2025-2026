from typing import Optional, List
from .attribute import Attribute, VariantAttributeLink
from .product import Product
from sqlmodel import SQLModel, Field, Relationship

class VariantDefault(SQLModel):
    price: int
    stock: int

class VariantCreate(VariantDefault):
    product_id: int = None
    attribute_ids: Optional[List[int]] = None

class VariantUpdate(SQLModel):
    price: Optional[int] = None
    stock: Optional[int] = None
    product_id: Optional[int] = None
    attribute_ids: Optional[List[int]] = None

class VariantRead(VariantDefault):
    id: int = None
    product: Product = None
    attributes: List[Attribute] = []

class Variant(VariantDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(default=None, foreign_key="product.id")
    product: Product = Relationship(back_populates="variants")
    attributes: Optional[List[Attribute]] = Relationship(back_populates="variants", link_model=VariantAttributeLink)
