from fastapi import HTTPException
from sqlmodel import select

from models.attribute import Attribute
from models.variant import Variant
from schemas.variant import VariantCreate, VariantUpdate


class VariantService:
    def get_all(self, session):
        return session.exec(select(Variant)).all()

    def get_by_id(self, variant_id: int, session):
        return session.get(Variant, variant_id)

    def create(self, variant: VariantCreate, session):
        db_variant = Variant.model_validate(variant)

        if variant.attribute_ids is not None:
            new_attributes = (
                session.query(Attribute).filter(Attribute.id.in_(variant.attribute_ids)).all()
            )
            db_variant.attributes = new_attributes

        session.add(db_variant)
        session.commit()
        session.refresh(db_variant)
        return {"status": 200, "data": db_variant}

    def delete(self, variant_id: int, session):
        variant = session.get(Variant, variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        session.delete(variant)
        session.commit()
        return {"ok": True}

    def update(self, variant_id: int, variant: VariantUpdate, session):
        db_variant = session.get(Variant, variant_id)
        if not db_variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        variant_data = variant.model_dump(exclude_unset=True)

        for key, value in variant_data.items():
            if key != "attribute_ids":
                setattr(db_variant, key, value)

        attribute_ids = variant_data.get("attribute_ids")
        if attribute_ids is not None:
            new_attributes = (
                session.query(Attribute).filter(Attribute.id.in_(attribute_ids)).all()
            )
            db_variant.attributes = new_attributes

        session.add(db_variant)
        session.commit()
        session.refresh(db_variant)
        return db_variant
