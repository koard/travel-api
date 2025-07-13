from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ProvinceBase(BaseModel):
    name: str
    is_secondary: bool = False  # False = เมืองหลัก, True = เมืองรอง


class ProvinceCreate(ProvinceBase):
    pass


class ProvinceUpdate(BaseModel):
    name: Optional[str] = None
    is_secondary: Optional[bool] = None


class Province(ProvinceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
