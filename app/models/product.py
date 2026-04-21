from typing import Optional, List
from pydantic import BaseModel
from .attribute import Attribute

class Product(BaseModel):
    id: int
    name: str
    description: str
    attributes: Optional[List[Attribute]] = []
