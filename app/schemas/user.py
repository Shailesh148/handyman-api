from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field
from .service_type import ServiceTypePublic

class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    MECHANIC = "MECHANIC"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"


class UserCreate(BaseModel):
    full_name: str = Field(..., max_length=150)
    phone: str = Field(..., max_length=20)
    email: Optional[EmailStr] = None
    # For now you can keep this fixed to CUSTOMER on frontend if you like
    role: UserRole = UserRole.CUSTOMER
    service_type_ids: Optional[List[int]] = None


class UserRead(BaseModel):
    id: int
    auth0_user_id: str
    full_name: str
    phone: str
    email: Optional[EmailStr]
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True  # for SQLAlchemy -> Pydantic


# 🔹 Public version: no DB id, no auth0_user_id
class UserPublic(BaseModel):
    id: int
    full_name: str
    phone: str
    email: Optional[EmailStr]
    role: UserRole
    is_active: bool
    mechanic_services: Optional[List[ServiceTypePublic]] = None

    class Config:
        from_attributes = True