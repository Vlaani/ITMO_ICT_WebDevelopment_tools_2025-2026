from typing import Optional
from sqlmodel import SQLModel

class PropertyDefault(SQLModel):
    property_name_id: int
    variant_id: int
    attribute_id: int
    value: str = ""


class PropertyUpdate(SQLModel):
    property_name_id: Optional[int] = None
    variant_id: Optional[int] = None
    attribute_id: Optional[int] = None
    value: Optional[str] = None


class PropertyRead(PropertyDefault):
    id: int
