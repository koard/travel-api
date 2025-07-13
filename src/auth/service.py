from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from src.models.user_model import User
from src.auth.utils import hash_password
from src.schemas.user_schema import UserCreateWithPassword


async def create_user_with_password(user_in: UserCreateWithPassword, db: AsyncSession) -> User:
    # เช็คว่า email ซ้ำไหม
    result = await db.exec(select(User).where(User.email == user_in.email))
    existing_user = result.first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # สร้าง user ใหม่
    user = User(
        full_name=user_in.full_name,
        citizen_id=user_in.citizen_id,
        phone=user_in.phone,
        province_id=user_in.province_id,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
