from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.schemas.schemas import UserCreate, UserResponse
from app.models.models import Users
from app.database import get_db


route = APIRouter(
    tags=["Register"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@route.post('/register', response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = pwd_context.hash(user.password)
    new_user = Users(username = user.username, email = user.email, hashed_password = hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
