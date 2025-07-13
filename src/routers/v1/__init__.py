from fastapi import APIRouter

from .province_router import router as province_router
from .user_router import router as user_router
from .tax_router import router as tax_router


router = APIRouter()
router.include_router(province_router, tags=["Provinces"])
router.include_router(user_router, tags=["Users"])
router.include_router(tax_router, tags=["Tax"])
