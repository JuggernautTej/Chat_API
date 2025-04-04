"""This script handles password security (hashing and verification)
and token generation (creation and encoding access tokens with
expiration details) for the chat application."""

from app.core.config import settings
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Any, Union, Optional

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create access token
def create_access_token(
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None) -> str:
    """Creates an access token.
    Args:
        subject (Union[str, Any]): The subject of the token. Typically the user ID or can be a string or any other type of data (e.g., user info).
        expires_delta (Optional[timedelta], optional): The expiration time. Defaults to None.
    Returns:
        str: The access token"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain text password matches a hashed password.
    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.
    Returns:
        bool: True if the password matches, False otherwise."""
    return pwd_context.verify(plain_password, hashed_password)

# Function to get password hash
def get_password_hash(password: str) -> str:
    """Generates a hashed password.
    Args:
        password (str): The password to hash.
    Returns:
        str: The hashed password."""
    return pwd_context.hash(password)
