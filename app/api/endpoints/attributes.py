from fastapi import APIRouter, Depends

from db.db import get_session
from models.attribute import Attribute
from schemas.attribute import AttributeDefault, AttributeRead, AttributeUpdate
from services.attribute_service import AttributeService

router = APIRouter()
attribute_service = AttributeService()


@router.get("/attributes", response_model=list[AttributeRead])
def attributes_get(session=Depends(get_session)):
    return attribute_service.get_all(session)


@router.get("/attributes/{attribute_id}", response_model=AttributeRead)
def attribute_get(attribute_id: int, session=Depends(get_session)) -> Attribute:
    return attribute_service.get_by_id(attribute_id, session)


@router.post("/attributes")
def attribute_create(attribute: AttributeDefault, session=Depends(get_session)):
    return attribute_service.create(attribute, session)


@router.delete("/attributes/delete/{attribute_id}")
def attribute_delete(attribute_id: int, session=Depends(get_session)):
    return attribute_service.delete(attribute_id, session)


@router.patch("/attributes/{attribute_id}", response_model=AttributeRead)
def attribute_update(attribute_id: int, attribute: AttributeUpdate, session=Depends(get_session)) -> Attribute:
    return attribute_service.update(attribute_id, attribute, session)