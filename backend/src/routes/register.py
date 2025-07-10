from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas.schemas import UserCreate, UserResponse
from src.models.models import Users
from src.core.auth import get_password_hash
from src.database import get_db


route = APIRouter(
    tags=["Register"]
)


@route.post('/register', response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existed_user = db.query(Users).filter(Users.username == user.username | Users.email == user.email).first()
    if existed_user:
        raise HTTPException(
            status_code=400, 
            detail="Username or Email already exists!"  
        )
    hashed_pw = get_password_hash(user.password)
    new_user = Users(
        username = user.username, 
        email = user.email, 
        hashed_password = hashed_pw
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
