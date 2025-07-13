from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user_model import User


class ProvinceBase(SQLModel):
    name: str = Field(index=True, unique=True)
    is_secondary: bool = False  # True = เมืองรอง, False = เมืองหลัก


class Province(ProvinceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    users: List["User"] = Relationship(back_populates="province")
