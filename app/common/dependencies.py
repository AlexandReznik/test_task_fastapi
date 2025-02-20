from fastapi import Depends
from app.users.crud import get_current_user


def require_auth(user: dict = Depends(get_current_user)):
    return user