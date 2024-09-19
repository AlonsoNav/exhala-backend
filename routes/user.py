import random
import string
from datetime import datetime, timedelta
from pymongo import errors
from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import db
from schemas.user import UserCreate
from services.auth import create_cookie
from services.email import send_reset_email
from utils.pwdhash import verify_password, hash_password

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@user_router.post("/login", response_model=dict, tags=["auth"])
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Authenticate user and set access token cookie.
    """
    try:
        user = db.user.find_one({"email": form_data.username})
    except errors.PyMongoError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    create_cookie(response, user['email'])

    return {"message": "Login successful"}


@user_router.post('/signup', response_model=dict, tags=["auth"])
async def signup(response: Response, item: UserCreate) -> dict:
    """
    Register a new user and set access token cookie.
    """
    try:
        if db.user.find_one({"email": item.email}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    except errors.PyMongoError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    new_user = dict(item)
    new_user['password'] = hash_password(new_user['password'])

    try:
        db.user.insert_one(new_user)
    except errors.PyMongoError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    create_cookie(response, new_user['email'])

    return {"message": "User created successfully"}


@user_router.post("/logout", response_model=dict, tags=["auth"])
async def logout(response: Response) -> dict:
    """
    Logout user by deleting access token cookie.
    """
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@user_router.post("/forgot-password")
async def forgot_password(email: str):
    user = db.user.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # Random 6-character code

    db.user.update_one(
        {"email": email},
        {"$set": {"reset_code": reset_code, "reset_code_expiration": datetime.utcnow() + timedelta(minutes=15)}}
    )

    await send_reset_email(email, reset_code)

    return {"message": "Reset code sent to your email"}


@user_router.post("/reset-password")
async def update_password(email: str, reset_code: str, new_password: str):
    user = db.user.find_one({"email": email})

    if not user or user.get("reset_code") != reset_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset code")

    if datetime.utcnow() > user["reset_code_expiration"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset code expired")

    hashed_password = hash_password(new_password)
    db.user.update_one(
        {"email": email},
        {"$set": {"password": hashed_password, "reset_code": None, "reset_code_expiration": None}}
    )

    return {"message": "Password successfully reset"}
