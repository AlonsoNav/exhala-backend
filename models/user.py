from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: EmailStr
    phone: int
    password: str
