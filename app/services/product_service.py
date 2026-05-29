from fastapi import HTTPException
from sqlmodel import select

from models.attribute import Attribute
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def get_all(self, session):
        return session.exec(select(Product)).all()

    def get_by_id(self, product_id: int, session):
        return session.get(Product, product_id)

    def create(self, product: ProductCreate, session):
        db_product = Product.model_validate(product)

        if product.attribute_ids is not None:
            new_attributes = (
                session.query(Attribute)
                .filter(Attribute.id.in_(product.attribute_ids))
                .all()
            )
            db_product.attributes = new_attributes

        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return {"status": 200, "data": db_product}

    def delete(self, product_id: int, session):
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return {"ok": True}

    def update(self, product_id: int, product: ProductUpdate, session):
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        product_data = product.model_dump(exclude_unset=True)

        for key, value in product_data.items():
            if key != "attribute_ids":
                setattr(db_product, key, value)

        attribute_ids = product_data.get("attribute_ids")
        if attribute_ids is not None:
            new_attributes = (
                session.query(Attribute).filter(Attribute.id.in_(attribute_ids)).all()
            )
            db_product.attributes = new_attributes

        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product
