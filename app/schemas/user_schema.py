from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from app.models.user import RoleEnum

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=6)
    role: RoleEnum

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: RoleEnum

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
