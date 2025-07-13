from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ... import models
from ...schemas import province_schema

router = APIRouter(prefix="/v1/provinces", tags=["Provinces"])


@router.get("/", response_model=list[province_schema.Province])
async def get_all_provinces(
    session: AsyncSession = Depends(models.get_session),
):
    statement = select(models.Province)
    result = await session.exec(statement)
    return result.all()


@router.post("/", response_model=province_schema.Province, status_code=status.HTTP_201_CREATED)
async def create_province(
    province: province_schema.ProvinceCreate,
    session: AsyncSession = Depends(models.get_session),
):
    db_province = models.Province.model_validate(province)
    session.add(db_province)
    await session.commit()
    await session.refresh(db_province)
    return db_province


@router.get("/{province_id}", response_model=province_schema.Province)
async def get_province_by_id(
    province_id: int,
    session: AsyncSession = Depends(models.get_session),
):
    province = await session.get(models.Province, province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    return province


@router.put("/{province_id}", response_model=province_schema.Province)
async def update_province(
    province_id: int,
    province_update: province_schema.ProvinceUpdate,
    session: AsyncSession = Depends(models.get_session),
):
    db_province = await session.get(models.Province, province_id)
    if not db_province:
        raise HTTPException(status_code=404, detail="Province not found")

    for key, value in province_update.model_dump(exclude_unset=True).items():
        setattr(db_province, key, value)

    await session.commit()
    await session.refresh(db_province)
    return db_province


@router.delete("/{province_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_province(
    province_id: int,
    session: AsyncSession = Depends(models.get_session),
):
    db_province = await session.get(models.Province, province_id)
    if not db_province:
        raise HTTPException(status_code=404, detail="Province not found")

    await session.delete(db_province)
    await session.commit()
