import jwt  # For Json Web Token
import os
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException, status, Request, Response
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: Dict, expires_delta: timedelta = timedelta(days=7)):
    """
    Create a new access token with the given data and expiration time
    :param data: dict: payload
    :param expires_delta: timedelta: expiration time
    :return: str: access token
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Dict:
    """
    Verify the given token and return the payload
    :param token: str: token
    :return: dict: payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def verify_user(request: Request) -> Dict:
    """
    Verify the user by checking the token in the request
    :param request:
    :return: dict: payload
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    return verify_token(token)


def create_cookie(response: Response, email: str):
    """
    Create a new access token and set it in the response cookies
    :param response: Response
    :param email: str
    """
    token = create_access_token(data={"sub": email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=604800,  # 1 week
    )
