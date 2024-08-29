import bcrypt
from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import db
from schemas.user import user_entity, user_list_entity
from models.user import User
from bson import ObjectId
from services.auth import create_access_token

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


@user_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.user.find_one({"email": form_data.username})

    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(data={"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


@user_router.get('/users', response_model=list[User], tags=['users'])
async def find_all_users():
    return user_list_entity(db.user.find())


@user_router.post('/users', response_model=User, tags=['users'])
async def create_user(item: User):
    new_user = dict(item)
    new_user['password'] = hash_password(new_user['password'])
    user_id = db.user.insert_one(dict(new_user)).inserted_id
    return str(user_id)


@user_router.get('/users/{user_id}', response_model=User, tags=['users'])
async def find_user(user_id: str):
    return user_entity(db.user.find_one({"_id": ObjectId(user_id)}))


@user_router.put('/users/{user_id}', response_model=User, tags=['users'])
async def update_user(user_id: str, item: User):
    db.user.update_one({"_id": ObjectId(user_id)}, {'$set': dict(item)})


@user_router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
async def delete_user(user_id: str):
    db.user.delete_one({"_id": ObjectId(user_id)})
    return Response(status_code=status.HTTP_204_NO_CONTENT)
