from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserDB(UserBase):
    hashed_password: str

class CreateUser(UserBase):
    password: str