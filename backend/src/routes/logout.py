from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user, oauth2_scheme
from src.database import get_db
from src.models.models import TokenBlacklist, RefreshToken


route = APIRouter(
    tags=["logout"]
)


@route.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    blacklisted = TokenBlacklist(token = token)
    db.add(blacklisted)
    db.commit()
    refresh_token_entry = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if refresh_token_entry:
        refresh_token_entry.is_expired = True
        db.commit()
    return "Logged out successfully!"