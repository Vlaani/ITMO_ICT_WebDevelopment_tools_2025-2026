from fastapi import APIRouter, FastAPI
from typing import List
from typing_extensions import TypedDict
from models.variant import Variant
from db.temp_db import temp_db

router = APIRouter()

@router.get("/variants")
def variants_get():
    return temp_db

@router.get("/variants/{variant_id}")
def variant_get(variant_id: int) -> List[Variant]:
    return [variant for variant in temp_db if variant.get("id") == variant_id]

@router.post("/variants")
def variant_create(variant: Variant) -> TypedDict('Response', {"status": int, "data": Variant}):
    temp_db.append(variant)
    return {"status": 200, "data": variant}

@router.delete("/variants/delete/{variant_id}")
def variant_delete(variant_id: int):
    for i, variant in enumerate(temp_db):
        if variant.get("id") == variant_id:
            temp_db.pop(i)
            break
    return {"status": 201, "message": "deleted"}

@router.put("/variants/{variant_id}")
def variant_update(variant_id: int, variant: Variant) -> List[Variant]:
    for i, var in enumerate(temp_db):
        if var.get("id") == variant_id:
            temp_db[i] = variant
    return temp_db