from itertools import product

from fastapi import HTTPException
from sqlmodel import select

from db.db import get_session
from models.order import Order, OrderVariantLink, OrderStatus
from models.variant import Variant
from schemas.order import OrderCreate, OrderRead, OrderVariantItemRead
from services.security_service import SecurityService


class OrderService:
    def __init__(self):
        self.security_service = SecurityService()

    def get_orders_by_user(self, current_user):
        return current_user.orders

    def create_order(self, current_user, order: OrderCreate, session):
        variant_ids = [item.variant_id for item in order.items]
        variants = session.query(Variant).filter(Variant.id.in_(variant_ids)).all()
        variant_map = {v.id: v for v in variants}
        
        total_price = 0
        link_items = []
        
        for item in order.items:
            variant = variant_map[item.variant_id]

            if not variant:
                raise HTTPException(status_code=404, detail=f"Variant {item.variant_id} not found")
            
            if variant.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for variant {variant.id}")
            
            variant.stock -= item.quantity

            total_price += variant.price * item.quantity
            
            link_items.append(OrderVariantLink(variant_id=item.variant_id, quantity=item.quantity))

        db_order = Order(
            user_id=current_user.id,
            total_price=total_price,
            items=link_items
        )
        
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order

    def cancel_order(self, current_user, order_id: int, session):
        order = session.exec(select(Order).where(Order.id == order_id, Order.user_id == current_user.id)).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found or access denied")

        if order.status == OrderStatus.shipped:
            raise HTTPException(status_code=400, detail="Cannot cancel a shipped order")

        for link in order.items:
            variant = session.get(Variant, link.variant_id)
            if variant:
                variant.stock += link.quantity
                session.add(variant)

        order.status = OrderStatus.canceled
        
        session.add(order)
        session.commit()
        session.refresh(order)
        
        return order
