from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from schemas import PropertyDefault, PropertyUpdate, PropertyRead

if TYPE_CHECKING:
    from .attribute_name import AttributeName
    from .property import Property
    from .product import Product
    from .variant import Variant
    from .attribute import Attribute

class ProductAttributeLink(SQLModel, table=True):
    product_id: int = Field(default=None, foreign_key="product.id", primary_key=True)
    attribute_id: int = Field(default=None, foreign_key="attribute.id", primary_key=True)

class VariantAttributeLink(SQLModel, table=True):
    variant_id: int = Field(default=None, foreign_key="variant.id", primary_key=True)
    attribute_id: int = Field(default=None, foreign_key="attribute.id", primary_key=True)
    variant: "Variant" = Relationship(back_populates="attribute_links")
    attribute: "Attribute" = Relationship()
    properties: List["Property"] = Relationship(back_populates="variant_attribute_link")

class Attribute(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    attribute_name_id: int = Field(default=None, foreign_key="attributename.id")
    value: str = ""
    attribute_name: "AttributeName" = Relationship()
    products: List["Product"] = Relationship(back_populates="attributes", link_model=ProductAttributeLink)
    variants: List["Variant"] = Relationship(back_populates="attributes", link_model=VariantAttributeLink)
