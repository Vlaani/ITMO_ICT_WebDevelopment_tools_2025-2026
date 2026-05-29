from fastapi import APIRouter
from .endpoints import (
    variants,
    attributes,
    products,
    users,
    orders,
    auth,
    attribute_names,
    property_names,
    properties,
)

router = APIRouter()
router.include_router(variants.router)
router.include_router(attributes.router)
router.include_router(attribute_names.router)
router.include_router(property_names.router)
router.include_router(properties.router)
router.include_router(products.router)
router.include_router(users.router)
router.include_router(orders.router)
router.include_router(auth.router)