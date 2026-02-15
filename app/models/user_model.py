from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId

class UserBase(BaseModel):
    email: EmailStr
    plan: Literal["FREE", "PRO", "ULTRA", "BUSINESS"] = "FREE"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    daily_requests: int = 0
    last_request_date: Optional[str] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True

class UserInDB(UserBase):
    _id: ObjectId
    password_hash: str
    daily_requests: int = 0
    last_request_date: Optional[str] = None
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class QuotaStatus(BaseModel):
    plan: str
    daily_limit: int
    daily_requests: int
    remaining: int
    quota_exceeded: bool

class PlanUpgrade(BaseModel):
    new_plan: Literal["FREE", "PRO", "ULTRA", "BUSINESS"]