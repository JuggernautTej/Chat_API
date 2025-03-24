"""Initialize the database with the initial admin user if it does not exist."""

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.database import async_session_maker as async_session
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, List, Union
import asyncio

# Asynchronous function to initialize the database
async def init_db() -> None:
    """The function to initialize the database.
    Args:
        None
    Returns:
        None
    """
    # Create the database tables
    async with async_session() as session:
        await create_initial_admin(session)

async def create_initial_admin(session: AsyncSession) -> None:
    """The function to create the initial admin user.
    Args:
        session (AsyncSession): The database session
    Returns:
        None
    """
    admin_email = settings.FIRST_ADMIN_EMAIL
    if admin_email:
        existing_admin = await session.execute(select(User).filter(User.email == admin_email))
        admin = existing_admin.scalars().first()

        if not admin:
            admin_user = User(
                email=admin_email,
                username=settings.FIRST_ADMIN_USERNAME,
                hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
                is_active=True)
            session.add(admin_user)
            await session.commit()
