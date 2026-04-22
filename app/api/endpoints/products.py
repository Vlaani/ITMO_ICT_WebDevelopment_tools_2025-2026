from fastapi import APIRouter, FastAPI, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select
from models.product import *
from db.db import get_session

router = APIRouter()

@router.get("/products", response_model=list[ProductRead])
def products_get(session=Depends(get_session)):
    return session.exec(select(Product)).all()

@router.get("/products/{product_id}", response_model=ProductRead)
def product_get(product_id: int, session=Depends(get_session)) -> Product:
    return session.get(Product, product_id)

@router.post("/products")
def product_create(product: ProductCreate, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": ProductRead}):
    db_product = Product.model_validate(product)
    
    if product.attribute_ids is not None:
        new_attributes = session.query(Attribute).filter(Attribute.id.in_(product.attribute_ids)).all()
        db_product.attributes = new_attributes

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return {"status": 200, "data": db_product}

@router.delete("/products/delete/{product_id}")
def product_delete(product_id: int, session=Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"ok": True}

@router.patch("/products/{product_id}", response_model=ProductRead)
def product_update(product_id: int, product: ProductUpdate, session=Depends(get_session)) -> Product:
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product.model_dump(exclude_unset=True)
    
    for key, value in product_data.items():
        if key != "attribute_ids":
            setattr(db_product, key, value)

    if product_data["attribute_ids"] is not None:
        new_attributes = session.query(Attribute).filter(Attribute.id.in_(product_data["attribute_ids"])).all()
        db_product.attributes = new_attributes

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product