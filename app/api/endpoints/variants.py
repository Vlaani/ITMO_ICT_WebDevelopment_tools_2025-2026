from fastapi import APIRouter, Depends

from models.variant import Variant
from schemas.variant import VariantCreate, VariantRead, VariantUpdate
from db.db import get_session
from services.variant_service import VariantService

router = APIRouter()
variant_service = VariantService()


@router.get("/variants", response_model=list[VariantRead])
def variants_get(session=Depends(get_session)):
    return variant_service.get_all(session)


@router.get("/variants/{variant_id}", response_model=VariantRead)
def variant_get(variant_id: int, session=Depends(get_session)) -> Variant:
    return variant_service.get_by_id(variant_id, session)


@router.post("/variants")
def variant_create(variant: VariantCreate, session=Depends(get_session)):
    return variant_service.create(variant, session)


@router.delete("/variants/delete/{variant_id}")
def variant_delete(variant_id: int, session=Depends(get_session)):
    return variant_service.delete(variant_id, session)


@router.patch("/variants/{variant_id}", response_model=VariantRead)
def variant_update(variant_id: int, variant: VariantUpdate, session=Depends(get_session)) -> Variant:
    return variant_service.update(variant_id, variant, session)