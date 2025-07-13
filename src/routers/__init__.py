from fastapi import APIRouter

from .v1.province_router import router as province_router
from .v1.user_router import router as user_router

router = APIRouter()
router.include_router(province_router)
router.include_router(user_router)
