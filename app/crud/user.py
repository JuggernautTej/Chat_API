"""CRUD operations for user model."""

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, List, Optional, Union
from uuid import UUID


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Create a new user."""
    user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=get_password_hash(user.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
    """Get a user by id."""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get a user by email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get a user by username."""
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination."""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def update_user(db: AsyncSession, user_id: UUID, user_in: Union[UserUpdate, Dict[str, Any]]) -> Optional[User]:
    """Updates an existing user's information."""
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Convert input to dictionary if it's a Pydantic model
    if not isinstance(user_in, dict):
        user_in = user_in.model_dump(exclude_unset=True)
    
    # Handle password update separately
    if "password" in user_in:
        user_in["hashed_password"] = get_password_hash(user_in["password"])
        del user_in["password"]

    # Update user fields
    for key, value in user_in.items():
        setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: UUID) -> Optional[User]:
    """Delete a user."""
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    await db.delete(user)
    await db.commit()
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
