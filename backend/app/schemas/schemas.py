from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UpdateNote(BaseModel):
    note_title: str
    note_content: str

class TakeNote(BaseModel):
    owner_id: str
    note_title: str
    note_content: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# class CheckNote(BaseModel):
#     owner: str
#     note_title: str
#     note_content: str
#     create_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True