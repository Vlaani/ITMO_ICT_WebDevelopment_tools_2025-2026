from fastapi import APIRouter, Depends

from db.db import get_session
from models.property import Property
from schemas.property import PropertyDefault, PropertyRead, PropertyUpdate
from services.property_service import PropertyService

router = APIRouter()
property_service = PropertyService()


@router.get("/properties", response_model=list[PropertyRead])
def properties_get(session=Depends(get_session)):
    return property_service.get_all(session)


@router.get("/properties/{property_id}", response_model=PropertyRead)
def property_get(property_id: int, session=Depends(get_session)) -> Property:
    return property_service.get_by_id(property_id, session)


@router.post("/properties")
def property_create(property_item: PropertyDefault, session=Depends(get_session)):
    return property_service.create(property_item, session)


@router.delete("/properties/delete/{property_id}")
def property_delete(property_id: int, session=Depends(get_session)):
    return property_service.delete(property_id, session)


@router.patch("/properties/{property_id}", response_model=PropertyRead)
def property_update(property_id: int, property_item: PropertyUpdate, session=Depends(get_session)) -> Property:
    return property_service.update(property_id, property_item, session)
