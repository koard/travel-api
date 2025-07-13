from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.models import User
from .schemas import LoginRequest, Token
from .utils import verify_password, create_access_token


async def login_user(data: LoginRequest, session: AsyncSession) -> Token:
    result = await session.exec(select(User).where(User.email == data.email))
    user = result.first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token({"user_id": user.id, "email": user.email})
    return Token(access_token=token)
