from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: str = "manager"
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# UserOut is a schema for responses that doesn't include sensitive information
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# TeamMember Schemas
class TeamMemberBase(BaseModel):
    first_name: str
    last_name: str
    position: Optional[str] = None
    email: EmailStr
    start_date: Optional[date] = None
    profile_picture_url: Optional[str] = None
    public_notes: Optional[str] = None
    manager_notes: Optional[str] = None
    superior_id: Optional[int] = None
    is_active: bool = True


class TeamMemberCreate(TeamMemberBase):
    user_id: Optional[int] = None


class TeamMemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    email: Optional[EmailStr] = None
    start_date: Optional[date] = None
    profile_picture_url: Optional[str] = None
    public_notes: Optional[str] = None
    manager_notes: Optional[str] = None
    superior_id: Optional[int] = None
    is_active: Optional[bool] = None
    user_id: Optional[int] = None


class TeamMember(TeamMemberBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TeamMemberWithReports(TeamMember):
    direct_reports: List["TeamMemberWithReports"] = []

    class Config:
        from_attributes = True


# Recursive reference resolution for TeamMemberWithReports
TeamMemberWithReports.update_forward_refs()


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    id: Optional[int] = None
