from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app.schemas.schemas import UserLogin
from app.database import get_db
from app.models.models import Users

route = APIRouter(
    tags=["Login"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@route.post('/login')
def login(login_request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == login_request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    if not pwd_context.verify(login_request.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid Password!")
    return "Login Successfully!"