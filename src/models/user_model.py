from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .province_model import Province


class UserBase(SQLModel):
    full_name: str = Field(index=True)
    citizen_id: str = Field(unique=True, index=True)
    phone: str
    province_id: int = Field(foreign_key="province.id")
    email: str = Field(unique=True, index=True) 
    hashed_password: str                      


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    province: Optional["Province"] = Relationship(back_populates="users")
