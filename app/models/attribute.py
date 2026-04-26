from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .product import Product
    from .variant import Variant

class ProductAttributeLink(SQLModel, table=True):
    product_id: int = Field(default=None, foreign_key="product.id", primary_key=True)
    attribute_id: int = Field(default=None, foreign_key="attribute.id", primary_key=True)

class VariantAttributeLink(SQLModel, table=True):
    variant_id: int = Field(default=None, foreign_key="variant.id", primary_key=True)
    attribute_id: int = Field(default=None, foreign_key="attribute.id", primary_key=True)

class Attribute(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = ""
    value: str = ""
    products: List['Product'] = Relationship(back_populates="attributes", link_model=ProductAttributeLink)
    variants: List['Variant'] = Relationship(back_populates="attributes", link_model=VariantAttributeLink)
