from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

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
    birthdate: Optional[datetime] = Field(None, description="The birthdate of the user")
    bio: Optional[str] = Field(None, description="The bio of the user")
    psychologistType: Optional[str] = Field(None, description="The type of psychologist")
    gender: Optional[str] = Field(None, description="The gender of the user")
    profile_image: Optional[str] = Field(None, description="The base64 encoded profile image of the user")

class UpdateUserRequest(BaseModel):
    """
    Schema for updating user data.
    """
    name: Optional[str] = Field(None, description="The name of the user")
    email: Optional[EmailStr] = Field(None, description="The email of the user")
    phone: Optional[str] = Field(None, description="The phone number of the user")
    address: Optional[str] = Field(None, description="The address of the user")
    birthdate: Optional[datetime] = Field(None, description="The birthdate of the user")
    bio: Optional[str] = Field(None, description="The bio of the user")
    psychologistType: Optional[str] = Field(None, description="The type of psychologist")
    gender: Optional[str] = Field(None, description="The gender of the user")

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

class ChangePasswordRequest(BaseModel):
    """
    Schema for change password request.
    """
    oldPassword: str = Field(..., description="The old password of the user")
    newPassword: str = Field(..., description="The new password of the user")