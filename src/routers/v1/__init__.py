from fastapi import APIRouter

from .province_router import router as province_router
from .user_router import router as user_router

router = APIRouter()
router.include_router(province_router, prefix="/province", tags=["province"])
router.include_router(user_router, prefix="/user", tags=["user"])
