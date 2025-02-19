from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.common.jwt import create_token, get_password_hash, verify_password
from app.users.model import User


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
