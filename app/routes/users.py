from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user

