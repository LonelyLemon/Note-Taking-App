from fastapi import APIRouter, Depends

from src.schemas.schemas import UserResponse
from src.models.models import Users
from src.core.auth import get_current_user


route = APIRouter(
    tags=["User"]
)


@route.get('/me', response_model=UserResponse)
def get_user(current_user: Users = Depends(get_current_user)):
    return current_user