from typing import Optional, List, TYPE_CHECKING
from .attribute import Attribute, ProductAttributeLink
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .variant import Variant


class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = ""
    description: Optional[str] = ""
    attributes: Optional[List[Attribute]] = Relationship(back_populates="products", link_model=ProductAttributeLink)
    variants: List['Variant'] = Relationship(back_populates="product")
