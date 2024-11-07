import random
import string
from datetime import datetime, timedelta, timezone
from pymongo import errors
from fastapi import APIRouter, status, HTTPException, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import db
from schemas.user import UserCreate, ForgotPasswordRequest, ResetPasswordRequest, UserResponse
from services.auth import create_cookie, verify_user
from services.email import send_reset_email
from utils.pwdhash import verify_password, hash_password
import logging

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_user_by_email(email: str):
    try:
        return db.user.find_one({"email": email})
    except errors.PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

def create_user_response(user: dict) -> UserResponse:
    return UserResponse(
        name=user["name"],
        email=user["email"],
        type=user["type"],
        phone=user.get("phone"),
        address=user.get("address"),
        birthdate=user.get("birthdate"),
        bio=user.get("bio"),
        psychologistType=user.get("psychologistType"),
        gender=user.get("gender")
    )

@user_router.post("/login", response_model=dict, tags=["auth"])
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Authenticate user and set access token cookie.
    """
    logger.info(f"Login attempt for {form_data.username}")
    user = find_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    create_cookie(response, user['email'])
    return {"message": "Login successful", "user": create_user_response(user)}

@user_router.post('/signup', response_model=dict, tags=["auth"])
async def signup(response: Response, item: UserCreate) -> dict:
    """
    Register a new user and set access token cookie.
    """
    if find_user_by_email(item.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = {k: v for k, v in dict(item).items() if v is not None}
    new_user['password'] = hash_password(new_user['password'])

    try:
        db.user.insert_one(new_user)
    except errors.PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    create_cookie(response, new_user['email'])
    return {"message": "User created successfully", "user": create_user_response(new_user)}

@user_router.post("/logout", response_model=dict, tags=["auth"])
async def logout(response: Response) -> dict:
    """
    Logout user by deleting access token cookie.
    """
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}

@user_router.post("/forgot-password", response_model=dict, tags=["auth"])
async def forgot_password(request: ForgotPasswordRequest):
    """"
    Send a reset code to user's email.
    """
    now_utc = datetime.now(timezone.utc)

    user = find_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # Random 6-character code
    db.user.update_one(
        {"email": request.email},
        {"$set": {"reset_code": reset_code, "reset_code_expiration": now_utc + timedelta(minutes=15)}}
    )

    await send_reset_email(request.email, reset_code)
    return {"message": "Reset code sent to your email"}

@user_router.post("/reset-password", response_model=dict, tags=["auth"])
async def update_password(request: ResetPasswordRequest):
    """
    Update user's password using reset code.
    :param request:
    :return:
    """
    now_utc = datetime.now(timezone.utc)

    user = find_user_by_email(request.email)
    if not user or user.get("reset_code") != request.code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset code")

    reset_code_expiration = user["reset_code_expiration"]
    if reset_code_expiration.tzinfo is None:
        reset_code_expiration = reset_code_expiration.replace(tzinfo=timezone.utc)

    if now_utc > reset_code_expiration:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset code expired")

    hashed_password = hash_password(request.password)
    db.user.update_one(
        {"email": request.email},
        {"$set": {"password": hashed_password, "reset_code": None, "reset_code_expiration": None}}
    )
    return {"message": "Password successfully reset"}

@user_router.get("/validate-cookie", response_model=UserResponse, tags=["auth"])
async def validate_cookie(request: Request):
    """
    Validate user's access token cookie.
    :param request:
    :return:
    """
    try:
        payload = verify_user(request)
        user = find_user_by_email(payload["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return create_user_response(user)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail="You must login again")
