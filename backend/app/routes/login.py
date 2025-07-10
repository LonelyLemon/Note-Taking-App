from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.models import Users
from app.utils.auth import create_access_token


route = APIRouter(
    tags=["Login"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@route.post('/login')
def login(login_request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == login_request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    if not pwd_context.verify(login_request.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid Password!")
    access_token = create_access_token(
        data = {"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}