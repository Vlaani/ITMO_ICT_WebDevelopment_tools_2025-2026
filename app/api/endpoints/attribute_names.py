from fastapi import APIRouter, Depends

from db.db import get_session
from models.attribute_name import AttributeName
from schemas.attribute_name import AttributeNameDefault, AttributeNameRead, AttributeNameUpdate
from services.attribute_name_service import AttributeNameService

router = APIRouter()
attribute_name_service = AttributeNameService()


@router.get("/attribute_names", response_model=list[AttributeNameRead])
def attribute_names_get(session=Depends(get_session)):
    return attribute_name_service.get_all(session)


@router.get("/attribute_names/{attribute_name_id}", response_model=AttributeNameRead)
def attribute_name_get(attribute_name_id: int, session=Depends(get_session)) -> AttributeName:
    return attribute_name_service.get_by_id(attribute_name_id, session)


@router.post("/attribute_names")
def attribute_name_create(attribute_name: AttributeNameDefault, session=Depends(get_session)):
    return attribute_name_service.create(attribute_name, session)


@router.delete("/attribute_names/delete/{attribute_name_id}")
def attribute_name_delete(attribute_name_id: int, session=Depends(get_session)):
    return attribute_name_service.delete(attribute_name_id, session)


@router.patch("/attribute_names/{attribute_name_id}", response_model=AttributeNameRead)
def attribute_name_update(attribute_name_id: int, attribute_name: AttributeNameUpdate, session=Depends(get_session)) -> AttributeName:
    return attribute_name_service.update(attribute_name_id, attribute_name, session)
