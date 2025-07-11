from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError
from datetime import datetime

from src.database import get_db
from src.core.auth import JWT_ALGORITHM, JWT_SECRET_KEY, create_access_token
from src.models.models import RefreshToken, Users

route = APIRouter(
    tags=["Refresh Token"]
)

@route.post('/refresh-token')
async def refresh_token(refresh_token: str, 
                        db: AsyncSession = Depends(get_db)
                        ) -> dict:
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid Token Type"
            )
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Refresh Token"
        )
    
    refresh_token_entry_result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token))
    refresh_token_entry = refresh_token_entry_result.scalars().first()

    if not refresh_token_entry or refresh_token_entry.is_expired:
        raise HTTPException(
            status_code=401,
            detail="Invalid Refresh Token"
        )
    
    if refresh_token_entry.expired_at < datetime.utcnow():
        refresh_token_entry.is_expired = True
        await db.commit()
        raise HTTPException(
            status_code=401,
            detail="Refresh Token Expired"
        )
    
    user_result = await db.execute(select(Users).where(Users.user_id == refresh_token_entry.user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found!"
        )

    new_access_token = create_access_token(
        data = {"sub": username}
    )
    return {"access_token": new_access_token}