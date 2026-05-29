"""attribute_name and property models

Revision ID: e3d90b1f4a1c
Revises: bb6884eed0c2
Create Date: 2026-05-12 13:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3d90b1f4a1c"
down_revision: Union[str, Sequence[str], None] = "bb6884eed0c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "attributename",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "propertyname",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("attribute", sa.Column("attribute_name_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_attribute_attribute_name_id_attributename",
        "attribute",
        "attributename",
        ["attribute_name_id"],
        ["id"],
    )

    op.execute(
        """
        INSERT INTO attributename (name)
        SELECT DISTINCT name
        FROM attribute
        WHERE name IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE attribute
        SET attribute_name_id = an.id
        FROM attributename an
        WHERE attribute.name = an.name
        """
    )

    op.alter_column("attribute", "attribute_name_id", nullable=False)
    op.drop_column("attribute", "name")

    op.create_table(
        "property",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("property_name_id", sa.Integer(), nullable=False),
        sa.Column("variant_id", sa.Integer(), nullable=False),
        sa.Column("attribute_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["property_name_id"], ["propertyname.id"]),
        sa.ForeignKeyConstraint(
            ["variant_id", "attribute_id"],
            ["variantattributelink.variant_id", "variantattributelink.attribute_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("property")
    op.add_column("attribute", sa.Column("name", sa.String(), nullable=True))

    op.execute(
        """
        UPDATE attribute
        SET name = an.name
        FROM attributename an
        WHERE attribute.attribute_name_id = an.id
        """
    )

    op.alter_column("attribute", "name", nullable=False)
    op.drop_constraint("fk_attribute_attribute_name_id_attributename", "attribute", type_="foreignkey")
    op.drop_column("attribute", "attribute_name_id")
    op.drop_table("propertyname")
    op.drop_table("attributename")
