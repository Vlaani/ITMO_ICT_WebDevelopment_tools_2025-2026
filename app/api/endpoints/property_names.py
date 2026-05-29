from fastapi import APIRouter, Depends

from db.db import get_session
from models.property_name import PropertyName
from schemas.property_name import PropertyNameDefault, PropertyNameRead, PropertyNameUpdate
from services.property_name_service import PropertyNameService

router = APIRouter()
property_name_service = PropertyNameService()


@router.get("/property_names", response_model=list[PropertyNameRead])
def property_names_get(session=Depends(get_session)):
    return property_name_service.get_all(session)


@router.get("/property_names/{property_name_id}", response_model=PropertyNameRead)
def property_name_get(property_name_id: int, session=Depends(get_session)) -> PropertyName:
    return property_name_service.get_by_id(property_name_id, session)


@router.post("/property_names")
def property_name_create(property_name: PropertyNameDefault, session=Depends(get_session)):
    return property_name_service.create(property_name, session)


@router.delete("/property_names/delete/{property_name_id}")
def property_name_delete(property_name_id: int, session=Depends(get_session)):
    return property_name_service.delete(property_name_id, session)


@router.patch("/property_names/{property_name_id}", response_model=PropertyNameRead)
def property_name_update(property_name_id: int, property_name: PropertyNameUpdate, session=Depends(get_session)) -> PropertyName:
    return property_name_service.update(property_name_id, property_name, session)
