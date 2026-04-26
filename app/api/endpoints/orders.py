from typing import Annotated
from fastapi import APIRouter, Depends, Header, HTTPException

from db.db import get_session
from schemas.order import OrderCreate, OrderRead
from schemas.user import UserReadFull
from services.order_service import OrderService
from services.auth_service import AuthService

router = APIRouter()
order_service = OrderService()
auth_service = AuthService()

@router.get("/orders/my", response_model=list[OrderRead])
def orders_my(current_user: Annotated[UserReadFull, Depends(auth_service.get_current_user)]):
    return order_service.get_orders_by_user(current_user)

@router.post("/orders/create", response_model=OrderRead)
def create(current_user: Annotated[UserReadFull, Depends(auth_service.get_current_user)], order: OrderCreate, session=Depends(get_session)):
    return order_service.create_order(current_user, order, session)

@router.post("/orders/cancel/{order_id}")
def cancel(current_user: Annotated[UserReadFull, Depends(auth_service.get_current_user)], order_id: int, session=Depends(get_session)):
    return order_service.cancel_order(current_user, order_id, session)