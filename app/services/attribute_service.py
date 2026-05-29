from fastapi import HTTPException
from sqlmodel import select

from models.attribute import Attribute
from models.attribute_name import AttributeName
from schemas.attribute import AttributeDefault, AttributeRead, AttributeUpdate


class AttributeService:
    def get_all(self, session) -> list[AttributeRead]:
        return session.exec(select(Attribute)).all()

    def get_by_id(self, attribute_id: int, session):
        return session.get(Attribute, attribute_id)

    def create(self, attribute: AttributeDefault, session):
        if not session.get(AttributeName, attribute.attribute_name_id):
            raise HTTPException(status_code=404, detail="AttributeName not found")
        db_attribute = Attribute.model_validate(attribute)
        session.add(db_attribute)
        session.commit()
        session.refresh(db_attribute)
        return {"status": 200, "data": db_attribute}

    def delete(self, attribute_id: int, session):
        attribute = session.get(Attribute, attribute_id)
        if not attribute:
            raise HTTPException(status_code=404, detail="Attribute not found")
        session.delete(attribute)
        session.commit()
        return {"ok": True}

    def update(self, attribute_id: int, attribute: AttributeUpdate, session):
        db_attribute = session.get(Attribute, attribute_id)
        if not db_attribute:
            raise HTTPException(status_code=404, detail="Attribute not found")

        attribute_data = attribute.model_dump(exclude_unset=True)
        if "attribute_name_id" in attribute_data:
            if not session.get(AttributeName, attribute_data["attribute_name_id"]):
                raise HTTPException(status_code=404, detail="AttributeName not found")
        for key, value in attribute_data.items():
            setattr(db_attribute, key, value)

        session.add(db_attribute)
        session.commit()
        session.refresh(db_attribute)
        return db_attribute
