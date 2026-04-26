from typing import TYPE_CHECKING, Optional, List
from .attribute import Attribute, VariantAttributeLink
from .order import OrderVariantLink
from .product import Product
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.order import Order


class Variant(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    price: int
    stock: int
    product_id: int = Field(default=None, foreign_key="product.id")
    product: Product = Relationship(back_populates="variants")
    attributes: Optional[List[Attribute]] = Relationship(back_populates="variants", link_model=VariantAttributeLink)
    orders: list["Order"] = Relationship(back_populates="variants", link_model=OrderVariantLink)
