from pydantic import BaseModel


class TaxRequest(BaseModel):
    province_name: str
    amount: float


class TaxResponse(BaseModel):
    province: str
    amount: float
    is_secondary: bool
    deductible: float
