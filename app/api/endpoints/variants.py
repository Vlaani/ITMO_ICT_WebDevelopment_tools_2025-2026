from fastapi import APIRouter, FastAPI, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select
from models.variant import *
from db.db import get_session

router = APIRouter()

@router.get("/variants", response_model=list[VariantRead])
def variants_get(session=Depends(get_session)):
    return session.exec(select(Variant)).all()

@router.get("/variants/{variant_id}", response_model=VariantRead)
def variant_get(variant_id: int, session=Depends(get_session)) -> Variant:
    return session.get(Variant, variant_id)

@router.post("/variants")
def variant_create(variant: VariantCreate, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": VariantRead}):
    db_variant = Variant.model_validate(variant)

    if variant.attribute_ids is not None:
        new_attributes = session.query(Attribute).filter(Attribute.id.in_(variant.attribute_ids)).all()
        db_variant.attributes = new_attributes

    session.add(db_variant)
    session.commit()
    session.refresh(db_variant)
    return {"status": 200, "data": db_variant}

@router.delete("/variants/delete/{variant_id}")
def variant_delete(variant_id: int, session=Depends(get_session)):
    variant = session.get(Variant, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    session.delete(variant)
    session.commit()
    return {"ok": True}

@router.patch("/variants/{variant_id}", response_model=VariantRead)
def variant_update(variant_id: int, variant: VariantUpdate, session=Depends(get_session)) -> Variant:
    db_variant = session.get(Variant, variant_id)
    if not db_variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    variant_data = variant.model_dump(exclude_unset=True)

    for key, value in variant_data.items():
        if key != "attribute_ids":
            setattr(db_variant, key, value)

    if variant_data["attribute_ids"] is not None:
        new_attributes = session.query(Attribute).filter(Attribute.id.in_(variant_data["attribute_ids"])).all()
        db_variant.attributes = new_attributes # SQLModel сам обновит связующую таблицу

    session.add(db_variant)
    session.commit()
    session.refresh(db_variant)
    return db_variant