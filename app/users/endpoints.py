from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.users.crud import authenticate_user, create_user
from app.users.schemas import TokenResponse, UserAuth, UserCreate, UserResponse


router = APIRouter()


@router.post("/sign-up/", response_model=UserResponse)
def registration(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.

    Args:
        user_data (UserCreate): The data of the user to be created, 
        including username, login, and password.
        db (Session): The database session to interact with the database.

    Returns:
        UserResponse: The created user object, serialized as a response.
    
    Raises:
        HTTPException: If a user with the same login already exists.
    """
    user = create_user(user_data.username, user_data.login, user_data.password, db)
    return user  


@router.post("/login/", response_model=TokenResponse)
def authorize(user_data: UserAuth, db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and return an access token.

    Args:
        user_data (UserAuth): The login and password credentials of the user.
        db (Session): The database session to interact with the database.

    Returns:
        TokenResponse: The generated JWT access token as a response.
    
    Raises:
        HTTPException: If the login or password is incorrect, or the user does not exist.
    """
    access_token = authenticate_user(user_data.login, user_data.password, db)
    return TokenResponse(token=access_token)
