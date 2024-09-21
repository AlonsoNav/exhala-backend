from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    name: str = Field(..., description="The name of the user")
    email: EmailStr = Field(..., description="The email of the user")
    password: str = Field(..., description="The password of the user")
    type: bool = Field(..., description="False for psychiatrist, True for patient")

class UserResponse(BaseModel):
    """
    Schema for user response.
    """
    name: str = Field(..., description="The name of the user")
    email: EmailStr = Field(..., description="The email of the user")
    type: bool = Field(..., description="False for psychiatrist, True for patient")
    phone: Optional[str] = Field(None, description="The phone number of the user")
    address: Optional[str] = Field(None, description="The address of the user")
    birthdate: Optional[date] = Field(None, description="The birthdate of the user")
    bio: Optional[str] = Field(None, description="The bio of the user")

class ForgotPasswordRequest(BaseModel):
    """
    Schema for forgot password request.
    """
    email: EmailStr = Field(..., description="The email of the user")

class ResetPasswordRequest(BaseModel):
    """
    Schema for reset password request.
    """
    email: EmailStr = Field(..., description="The email of the user")
    code: str = Field(..., description="The reset code sent to the user")
    password: str = Field(..., description="The new password of the user")