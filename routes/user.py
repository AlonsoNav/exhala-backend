import bcrypt
from fastapi import APIRouter, Response, status
from config.db import db
from schemas.user import user_entity, user_list_entity
from models.user import User
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()


@user.get('/users', response_model=list[User], tags=['users'])
def find_all_users():
    return user_list_entity(db.user.find())


@user.post('/users', response_model=User, tags=['users'])
def create_user(item: User):
    new_user = dict(item)
    pw = new_user['password'].encode('utf-8')
    new_user['password'] = bcrypt.hashpw(pw, bcrypt.gensalt())
    user_id = db.user.insert_one(dict(new_user)).inserted_id
    return str(user_id)


@user.get('/users/{user_id}', response_model=User, tags=['users'])
def find_user(user_id: str):
    return user_entity(db.user.find_one({"_id": ObjectId(user_id)}))


@user.put('/users/{user_id}', response_model=User, tags=['users'])
def update_user(user_id: str, item: User):
    db.user.update_one({"_id": ObjectId(user_id)}, {'$set': dict(item)})


@user.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_user(user_id: str):
    db.user.delete_one({"_id": ObjectId(user_id)})
    return Response(status_code=HTTP_204_NO_CONTENT)
