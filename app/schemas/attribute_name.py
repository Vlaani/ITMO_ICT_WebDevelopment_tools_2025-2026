from typing import Optional

from sqlmodel import SQLModel


class AttributeNameDefault(SQLModel):
    name: str = ""


class AttributeNameUpdate(SQLModel):
    name: Optional[str] = None


class AttributeNameRead(AttributeNameDefault):
    id: int
