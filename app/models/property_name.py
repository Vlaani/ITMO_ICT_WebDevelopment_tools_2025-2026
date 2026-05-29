from typing import List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .property import Property


class PropertyName(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = ""
    properties: List["Property"] = Relationship(back_populates="property_name")
