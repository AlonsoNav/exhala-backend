from bson import ObjectId
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

@psychologist_router.get("/psychologists/{id}", response_model=UserResponse, tags=["psychologist"])
async def get_psychologist_by_id(id: str, request: Request, current_user: dict = Depends(validate_cookie)):
    """
    Get a psychologist by their ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

    psychologist = db.user.find_one({"_id": ObjectId(id), "type": False})
    if not psychologist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Psychologist not found")

    return create_user_response(psychologist)
