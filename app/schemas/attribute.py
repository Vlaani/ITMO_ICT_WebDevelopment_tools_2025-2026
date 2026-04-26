from typing import Optional

from sqlmodel import SQLModel


class AttributeDefault(SQLModel):
    name: str = ""
    value: str = ""


class AttributeUpdate(SQLModel):
    name: Optional[str] = None
    value: Optional[str] = None


class AttributeRead(AttributeDefault):
    id: int
