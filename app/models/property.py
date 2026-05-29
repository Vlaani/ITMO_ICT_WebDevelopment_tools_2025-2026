from typing import TYPE_CHECKING

from sqlalchemy import ForeignKeyConstraint
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .attribute import VariantAttributeLink
    from .property_name import PropertyName

class Property(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["variant_id", "attribute_id"],
            ["variantattributelink.variant_id", "variantattributelink.attribute_id"],
        ),
    )

    id: int = Field(default=None, primary_key=True)
    property_name_id: int = Field(default=None, foreign_key="propertyname.id")
    variant_id: int = Field(default=None)
    attribute_id: int = Field(default=None)
    value: str = ""

    property_name: "PropertyName" = Relationship(back_populates="properties")
    variant_attribute_link: "VariantAttributeLink" = Relationship(back_populates="properties")
