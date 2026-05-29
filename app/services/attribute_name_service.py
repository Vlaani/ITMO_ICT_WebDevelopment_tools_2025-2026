from fastapi import HTTPException
from sqlmodel import select

from models.attribute_name import AttributeName
from schemas.attribute_name import AttributeNameDefault, AttributeNameUpdate


class AttributeNameService:
    def get_all(self, session):
        return session.exec(select(AttributeName)).all()

    def get_by_id(self, attribute_name_id: int, session):
        return session.get(AttributeName, attribute_name_id)

    def create(self, attribute_name: AttributeNameDefault, session):
        db_attribute_name = AttributeName.model_validate(attribute_name)
        session.add(db_attribute_name)
        session.commit()
        session.refresh(db_attribute_name)
        return {"status": 200, "data": db_attribute_name}

    def delete(self, attribute_name_id: int, session):
        attribute_name = session.get(AttributeName, attribute_name_id)
        if not attribute_name:
            raise HTTPException(status_code=404, detail="AttributeName not found")
        session.delete(attribute_name)
        session.commit()
        return {"ok": True}

    def update(self, attribute_name_id: int, attribute_name: AttributeNameUpdate, session):
        db_attribute_name = session.get(AttributeName, attribute_name_id)
        if not db_attribute_name:
            raise HTTPException(status_code=404, detail="AttributeName not found")

        attribute_name_data = attribute_name.model_dump(exclude_unset=True)
        for key, value in attribute_name_data.items():
            setattr(db_attribute_name, key, value)

        session.add(db_attribute_name)
        session.commit()
        session.refresh(db_attribute_name)
        return db_attribute_name
