"""This script houses the configuration settings for the chat app."""
from pydantic import BaseSettings, EmailStr, PostgresDsn
from typing import Optional


class Settings(BaseSettings):
    """The settings class defines the
    configuration settings for the chat app."""
    PROJECT_NAME: str = "Chat App"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: PostgresDsn

    # JWT Token Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Email Settings
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[EmailStr] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    # Admin User Settings
    FIRST_ADMIN_EMAIL: Optional[EmailStr] = None
    FIRST_ADMIN_USERNAME: Optional[str] = None
    FIRST_ADMIN_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
