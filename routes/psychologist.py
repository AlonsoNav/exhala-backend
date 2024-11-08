from fastapi import APIRouter, Depends, HTTPException, Request, status
from config.db import db
from schemas.user import UserResponse
from routes.user import validate_cookie, create_user_response
import logging

psychologist_router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@psychologist_router.get("/psychologists", response_model=list[UserResponse], tags=["psychologist"])
async def get_psychologists(request: Request, current_user: dict = Depends(validate_cookie)):
    """
    Get all users who are psychologists (type = False).
    """
    psychologists = list(db.user.find({"type": False}))
    return [create_user_response(psychologist) for psychologist in psychologists]