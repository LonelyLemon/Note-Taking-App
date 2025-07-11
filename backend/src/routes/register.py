from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from src.schemas.schemas import UserCreate, UserResponse
from src.models.models import Users
from src.core.auth import get_password_hash
from src.database import get_db


route = APIRouter(
    tags=["Register"]
)


@route.post('/register', response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(or_(Users.username == user.username, Users.email == user.email)))
    existed_user = result.scalars().first()
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
    await db.commit()
    await db.refresh(new_user)
    return new_user
