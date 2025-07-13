from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ...models import Province, get_session
from ...schemas import tax_schema

router = APIRouter(prefix="/v1/tax", tags=["Tax"])


@router.post("/calculate", response_model=tax_schema.TaxResponse)
async def calculate_tax_deduction(
    data: tax_schema.TaxRequest,
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Province).where(Province.name == data.province_name)
    result = await session.exec(stmt)
    province = result.first()

    if not province:
        raise HTTPException(status_code=404, detail="Province not found")

    rate = 0.2 if province.is_secondary else 0.1
    deductible = data.amount * rate

    return tax_schema.TaxResponse(
        province=province.name,
        amount=data.amount,
        is_secondary=province.is_secondary,
        deductible=deductible
    )
