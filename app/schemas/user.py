"""Pydantic schemas for user."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Shared properties
class UserBase(BaseModel):
    """Defines the user base class for shared user properties."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_online: Optional[bool] = False

# Properties to receive via API on creation
class UserCreate(UserBase):
    """This inherits from the user base class and adds specific fields for user creation."""
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    """This inherits from the user base class and adds specific fields for updating a user."""
    password: Optional[str] = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    """This extends UserBase and adds fields for user models stored in the database."""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """This class enables compartibility with ORM models."""
        orm_mode = True

# Properties to return to client
class User(UserInDBBase):
    """This class is used for returning data to clients."""
    pass

# Properties properties stored in DB
class UserInDB(UserInDBBase):
    """This class inherits from UserInDBBase and adds hashed password field."""
    hashed_password: str
