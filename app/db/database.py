"""The database connection settings for the chat app."""

from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator


# Database asynchronous connection settings
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=20,
    max_overflow=0, echo=True)

# Database session settings
async_session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine,
    class_=AsyncSession)

# Base class for the database
Base = declarative_base()

# Dependency to get the async database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """The function to get the database session.
    Args:
        None
    Returns:
        AsyncSession: The database session
    """
    async with async_session_maker() as session:
        yield session

