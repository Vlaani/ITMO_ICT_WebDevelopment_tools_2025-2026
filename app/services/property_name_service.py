from fastapi import HTTPException
from sqlmodel import select

from models.property_name import PropertyName
from schemas.property_name import PropertyNameDefault, PropertyNameUpdate


class PropertyNameService:
    def get_all(self, session):
        return session.exec(select(PropertyName)).all()

    def get_by_id(self, property_name_id: int, session):
        return session.get(PropertyName, property_name_id)

    def create(self, property_name: PropertyNameDefault, session):
        db_property_name = PropertyName.model_validate(property_name)
        session.add(db_property_name)
        session.commit()
        session.refresh(db_property_name)
        return {"status": 200, "data": db_property_name}

    def delete(self, property_name_id: int, session):
        property_name = session.get(PropertyName, property_name_id)
        if not property_name:
            raise HTTPException(status_code=404, detail="PropertyName not found")
        session.delete(property_name)
        session.commit()
        return {"ok": True}

    def update(self, property_name_id: int, property_name: PropertyNameUpdate, session):
        db_property_name = session.get(PropertyName, property_name_id)
        if not db_property_name:
            raise HTTPException(status_code=404, detail="PropertyName not found")

        property_name_data = property_name.model_dump(exclude_unset=True)
        for key, value in property_name_data.items():
            setattr(db_property_name, key, value)

        session.add(db_property_name)
        session.commit()
        session.refresh(db_property_name)
        return db_property_name
