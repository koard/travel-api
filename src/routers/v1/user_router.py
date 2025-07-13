from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ... import models
from ...schemas import user_schema
from src.auth.dependencies import get_current_user
from src.auth.utils import hash_password

router = APIRouter(prefix="/v1/users", tags=["Users"])


@router.get("/", response_model=list[user_schema.User])
async def get_all_users(session: AsyncSession = Depends(models.get_session)):
    statement = select(models.User)
    result = await session.exec(statement)
    return result.all()


@router.post("/", response_model=user_schema.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: user_schema.UserCreateWithPassword, session: AsyncSession = Depends(models.get_session)):
    hashed_password = hash_password(user.password)  
    db_user = models.User(
        full_name=user.full_name,
        citizen_id=user.citizen_id,
        phone=user.phone,
        province_id=user.province_id,
        email=user.email,
        hashed_password=hashed_password
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user



@router.get("/me")
async def read_user_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}


@router.get("/{user_id}", response_model=user_schema.User)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(models.get_session)):
    user = await session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=user_schema.User)
async def update_user(
    user_id: int,
    user_update: user_schema.UserUpdate,
    session: AsyncSession = Depends(models.get_session),
):
    db_user = await session.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(models.get_session),
):
    db_user = await session.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(db_user)
    await session.commit()
