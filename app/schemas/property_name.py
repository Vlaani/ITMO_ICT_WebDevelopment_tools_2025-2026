from typing import Optional

from sqlmodel import SQLModel


class PropertyNameDefault(SQLModel):
    name: str = ""


class PropertyNameUpdate(SQLModel):
    name: Optional[str] = None


class PropertyNameRead(PropertyNameDefault):
    id: int
