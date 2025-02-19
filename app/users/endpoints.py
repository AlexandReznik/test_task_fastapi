from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.users.crud import authenticate_user, create_user
from app.users.schemas import TokenResponse, UserAuth, UserCreate, UserResponse


router = APIRouter()


@router.post("/sign-up/", response_model=UserResponse)
def registration(user_data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(user_data.username, user_data.login, user_data.password, db)
    return user  


@router.post("/login/", response_model=TokenResponse)
def authorize(user_data: UserAuth, db: Session = Depends(get_db)):
    access_token = authenticate_user(user_data.login, user_data.password, db)
    return TokenResponse(token=access_token)
