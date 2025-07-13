from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    full_name: str
    citizen_id: str  # หมายเลขบัตรประชาชน
    phone: str
    province_id: int  # จังหวัดที่เลือกไปเที่ยว


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    citizen_id: Optional[str] = None
    phone: Optional[str] = None
    province_id: Optional[int] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserCreateWithPassword(UserBase):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    citizen_id: str
    phone: str
    province_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 