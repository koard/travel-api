from fastapi import APIRouter
from . import v1
from src.auth.router import router as auth_router

router = APIRouter()
router.include_router(v1.router)
router.include_router(auth_router)