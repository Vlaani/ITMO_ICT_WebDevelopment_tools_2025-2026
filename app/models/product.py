from typing import Optional, List, TYPE_CHECKING, Annotated
from .attribute import Attribute, ProductAttributeLink
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .variant import Variant
    #Annotated[ProductRead, FieldInfo(annotation=NoneType, required=True)]

class ProductDefault(SQLModel):
    name: str = ''
    description: Optional[str] = ""

class ProductCreate(SQLModel):
    name: str = ''
    description: Optional[str] = ""
    attribute_ids: Optional[List[int]] = None

class ProductUpdate(SQLModel):
    name: Optional[str] = ""
    description: Optional[str] = ""
    attribute_ids: Optional[List[int]] = None

class ProductVariant(SQLModel):
    id: int = None
    price: int = None
    stock: int = None
    attributes: List[Attribute] = []

class ProductRead(ProductDefault):
    id: int = None
    attributes: List[Attribute] = []
    variants: List[ProductVariant] = []

class Product(ProductDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    attributes: Optional[List[Attribute]] = Relationship(back_populates="products", link_model=ProductAttributeLink)
    variants: List['Variant'] = Relationship(back_populates="product")
