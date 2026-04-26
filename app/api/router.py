from fastapi import APIRouter
from .endpoints import variants, attributes, products, users, orders, auth

router = APIRouter()
router.include_router(variants.router)
router.include_router(attributes.router)
router.include_router(products.router)
router.include_router(users.router)
router.include_router(orders.router)
router.include_router(auth.router)