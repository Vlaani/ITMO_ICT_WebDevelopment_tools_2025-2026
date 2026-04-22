from fastapi import APIRouter
from .endpoints import variants, attributes, products

router = APIRouter()
router.include_router(variants.router)
router.include_router(attributes.router)
router.include_router(products.router)