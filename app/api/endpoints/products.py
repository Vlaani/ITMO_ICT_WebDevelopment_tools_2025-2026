from fastapi import APIRouter, Depends

from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from db.db import get_session
from services.product_service import ProductService

router = APIRouter()
product_service = ProductService()


@router.get("/products", response_model=list[ProductRead])
def products_get(session=Depends(get_session)):
    return product_service.get_all(session)


@router.get("/products/{product_id}", response_model=ProductRead)
def product_get(product_id: int, session=Depends(get_session)) -> ProductRead:
    return product_service.get_by_id(product_id, session)


@router.post("/products")
def product_create(product: ProductCreate, session=Depends(get_session)):
    return product_service.create(product, session)


@router.delete("/products/delete/{product_id}")
def product_delete(product_id: int, session=Depends(get_session)):
    return product_service.delete(product_id, session)


@router.patch("/products/{product_id}", response_model=ProductRead)
def product_update(product_id: int, product: ProductUpdate, session=Depends(get_session)) -> Product:
    return product_service.update(product_id, product, session)