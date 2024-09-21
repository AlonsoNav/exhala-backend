import jwt  # For Json Web Token
import os
from datetime import datetime, timedelta, timezone
from typing import Dict
from fastapi import HTTPException, status, Request, Response
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_access_token(data: Dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    """
    Create a new access token with the given data and expiration time.
    :param data: dict: Payload data
    :param expires_delta: timedelta: Expiration time
    :return: str: Encoded JWT token
    """
    now_utc = datetime.now(timezone.utc)
    to_encode = data.copy()
    to_encode.update({"exp": now_utc + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict:
    """
    Verify the given token and return the payload.
    :param token: str: JWT token
    :return: dict: Decoded payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Expired token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except jwt.PyJWTError:
        logger.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def verify_user(request: Request) -> Dict:
    """
    Verify the user by checking the token in the request.
    :param request: Request: FastAPI request object
    :return: dict: Decoded payload
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    return verify_token(token)

def create_cookie(response: Response, email: str):
    """
    Create a new access token and set it in the response cookies.
    :param response: Response: FastAPI response object
    :param email: str: User email
    """
    token = create_access_token(data={"sub": email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Set to True for better security
        secure=True,
        samesite="none",
        max_age=604800,  # 1 week
    )
