from fastapi import HTTPException
from sqlalchemy import and_
from sqlmodel import select

from models.attribute import VariantAttributeLink
from models.property import Property
from models.property_name import PropertyName
from schemas.property import PropertyDefault, PropertyUpdate


class PropertyService:
    def get_all(self, session):
        return session.exec(select(Property)).all()

    def get_by_id(self, property_id: int, session):
        return session.get(Property, property_id)

    def create(self, property_item: PropertyDefault, session):
        self._validate_refs(
            property_item.property_name_id,
            property_item.variant_id,
            property_item.attribute_id,
            session,
        )
        db_property = Property.model_validate(property_item)
        session.add(db_property)
        session.commit()
        session.refresh(db_property)
        return {"status": 200, "data": db_property}

    def delete(self, property_id: int, session):
        property_item = session.get(Property, property_id)
        if not property_item:
            raise HTTPException(status_code=404, detail="Property not found")
        session.delete(property_item)
        session.commit()
        return {"ok": True}

    def update(self, property_id: int, property_item: PropertyUpdate, session):
        db_property = session.get(Property, property_id)
        if not db_property:
            raise HTTPException(status_code=404, detail="Property not found")

        property_data = property_item.model_dump(exclude_unset=True)
        property_name_id = property_data.get("property_name_id", db_property.property_name_id)
        variant_id = property_data.get("variant_id", db_property.variant_id)
        attribute_id = property_data.get("attribute_id", db_property.attribute_id)
        self._validate_refs(property_name_id, variant_id, attribute_id, session)

        for key, value in property_data.items():
            setattr(db_property, key, value)

        session.add(db_property)
        session.commit()
        session.refresh(db_property)
        return db_property

    def _validate_refs(self, property_name_id: int, variant_id: int, attribute_id: int, session):
        if not session.get(PropertyName, property_name_id):
            raise HTTPException(status_code=404, detail="PropertyName not found")
        variant_attribute_link = session.exec(
            select(VariantAttributeLink).where(
                and_(
                    VariantAttributeLink.variant_id == variant_id,
                    VariantAttributeLink.attribute_id == attribute_id,
                )
            )
        ).first()
        if not variant_attribute_link:
            raise HTTPException(status_code=404, detail="VariantAttributeLink not found")
