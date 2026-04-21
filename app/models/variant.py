from typing import Optional, List
from pydantic import BaseModel
from .attribute import Attribute
from .product import Product

class Variant(BaseModel):
    id: int
    price: int
    stock: int
    product: Product
    attributes: Optional[List[Attribute]] = []
