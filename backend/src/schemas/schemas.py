from uuid import UUID

from pydantic import BaseModel, EmailStr
from datetime import datetime

#User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


#Note Schemas
class UpdateNote(BaseModel):
    note_title: str
    note_content: str

class TakeNote(BaseModel):
    owner_id: UUID
    note_title: str
    note_content: str


#Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str