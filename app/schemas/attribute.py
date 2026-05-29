from typing import Optional
from sqlmodel import SQLModel
from .attribute_name import AttributeNameDefault

class AttributeDefault(SQLModel):
    attribute_name: AttributeNameDefault
    value: str = ""


class AttributeUpdate(SQLModel):
    attribute_name_id: Optional[int] = None
    value: Optional[str] = None


class PropertyInVariantAttributeLinkRead(SQLModel):
    id: int
    property_name_id: int
    value: str = ""


class VariantAttributeLinkRead(SQLModel):
    variant_id: int
    attribute_id: int
    properties: list[PropertyInVariantAttributeLinkRead] = []


class AttributeRead(AttributeDefault):
    id: int
