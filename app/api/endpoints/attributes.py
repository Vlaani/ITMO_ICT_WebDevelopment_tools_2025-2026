from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlmodel import Session, create_engine, select
from typing_extensions import TypedDict
from typing import List
from db.db import get_session
from models.attribute import *

router = APIRouter()

@router.get("/attributes")
def attributes_get(session=Depends(get_session)):
    return session.exec(select(Attribute)).all()

@router.get("/attributes/{attribute_id}")
def attribute_get(attribute_id: int, session=Depends(get_session)) -> Attribute:
    return session.get(Attribute, attribute_id)

@router.post("/attributes")
def attribute_create(attribute: AttributeDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Attribute}):
    attribute = Attribute.model_validate(attribute)
    session.add(attribute)
    session.commit()
    session.refresh(attribute)
    #temp_db.append(attribute)
    return {"status": 200, "data": attribute}

@router.delete("/attributes/delete/{attribute_id}")
def attribute_delete(attribute_id: int, session=Depends(get_session)):
    attribute = session.get(Attribute, attribute_id)
    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    session.delete(attribute)
    session.commit()
    return {"ok": True}

@router.patch("/attributes/{attribute_id}")
def attribute_update(attribute_id: int, attribute: AttributeUpdate, session=Depends(get_session)) -> Attribute:
    db_attribute = session.get(Attribute, attribute_id)
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    attribute_data = attribute.model_dump(exclude_unset=True)
    for key, value in attribute_data.items():
        setattr(db_attribute, key, value)
    session.add(db_attribute)
    session.commit()
    session.refresh(db_attribute)
    return db_attribute