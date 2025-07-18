from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from src.database import get_db
from src.models.models import Users, RefreshToken
from src.core.auth import create_access_token, create_refresh_token, verify_password, REFRESH_TOKEN_EXPIRATION


route = APIRouter(
    tags=["Login"]
)


@route.post('/login')
async def login(login_request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Users).where(Users.username == login_request.username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    if not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Password!")
    access_token = create_access_token(
        data = {"sub": user.username}
    )

    #Create Refresh Token
    refresh_token = create_refresh_token(
        data = {"sub": user.username}
    )

    new_refresh_token = RefreshToken(
        token = refresh_token,
        user_id = user.user_id,
        expired_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION)
    )
    db.add(new_refresh_token)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token, 
        "token_type": "bearer"  
        }