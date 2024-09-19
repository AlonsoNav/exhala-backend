from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    type: bool  # False for psychiatrist, True for patient


class UserResponse(BaseModel):
    name: str
    email: EmailStr
    type: bool  # False for psychiatrist, True for patient
    phone: Optional[int] = None
    address: Optional[str] = None
    birthdate: Optional[date] = None
    bio: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    password: str
