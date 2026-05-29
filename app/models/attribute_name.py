from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

class AttributeName(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = ""
