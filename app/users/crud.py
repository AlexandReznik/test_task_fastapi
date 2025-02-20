from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.common.auth_utils import (create_token, get_password_hash,
                                   verify_password)
from app.common.database import get_db
from app.users.model import User
from app.common.auth_utils import decode_token


security = HTTPBearer()


def create_user(username: str, login: str, password: str, db: Session):
    if db.query(User).filter_by(login=login).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user = User(
        username=username,
        login=login,
        password=get_password_hash(password), 
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(login: str, password: str, db: Session):
    user = db.query(User).filter_by(login=login).first()
    if not user or not verify_password(password, user.password):  
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist"
        )

    return create_token(data={"sub": user.login})  


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security), 
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)
    return db.query(User).filter_by(login=payload['sub']).first()
