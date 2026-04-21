from fastapi import APIRouter
from .endpoints import variants

router = APIRouter()
router.include_router(variants.router)