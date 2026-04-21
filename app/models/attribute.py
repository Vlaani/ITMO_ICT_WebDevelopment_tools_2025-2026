from typing import Optional, List
from pydantic import BaseModel

class Attribute(BaseModel):
    id: int
    name: str
    value: int