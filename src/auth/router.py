from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.models.user_model import User
from src.schemas.user_schema import UserCreateWithPassword, UserRead
from src.auth.schemas import Token, LoginRequest
from src.auth.controller import login_user
from src.auth.service import create_user_with_password
from src.models import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    return await login_user(data, session)


@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreateWithPassword, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User).where(User.email == user.email))
    if result.first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = await create_user_with_password(user, session)
    return db_user
