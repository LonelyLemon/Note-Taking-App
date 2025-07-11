from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.auth import get_current_user, oauth2_scheme
from src.database import get_db
from src.models.models import TokenBlacklist, RefreshToken


route = APIRouter(
    tags=["logout"]
)


@route.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), 
                 db: AsyncSession = Depends(get_db), 
                 current_user: str = Depends(get_current_user)) -> dict:
    blacklisted = TokenBlacklist(token = token)
    db.add(blacklisted)
    db.commit()
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    refresh_token_entry = result.scalars().first()
    if refresh_token_entry:
        refresh_token_entry.is_expired = True
        await db.commit()
    return {"message": "Logged out successfully!"}