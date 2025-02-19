import os
from datetime import datetime, timedelta, timezone
from typing import Union

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

if not SECRET_KEY or not ALGORITHM:
    raise EnvironmentError("Environment variables SECRET_KEY and ALGORITHM must be set")


def create_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Args:
        data (dict): The data to encode in the JWT token.
        expires_delta (Union[timedelta, None], optional): 
            The duration for which the token is valid. 
            If None, the token expires in 15 minutes by default.

    Returns:
        str: The encoded JWT token as a string.

    Raises:
        EnvironmentError: If SECRET_KEY or ALGORITHM environment variables are not set.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    """
    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Args:
        plain_password (str): The plain-text password to be verified.
        hashed_password (str): The hashed password to compare with.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def decode_token(token: str):
    """
    Args:
        token (str): The JWT token to decode, typically provided by the OAuth2 scheme.

    Returns:
        dict: The decoded JWT payload if the token is valid.

    Raises:
        HTTPException: If the JWT token is invalid or expired, raises a 401 Unauthorized error.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")