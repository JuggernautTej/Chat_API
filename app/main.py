"""The main entry point of the application."""

from fastapi import FastAPI
from app.api.routes import users, auth, friends, messages, groups, notifications
from app.core.config import settings
from app.db.database import engine, Base
from contextlib import asynccontextmanager

# Create the database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to initialize and cleanup resources."""
    print("Staring up the application...")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield # Application runs here
    print("Shutting down the application...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # Drop the tables

# Initialize the FastAPI app
app = FastAPI(lifespan=lifespan)

# Include the routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(friends.router, prefix="/friends", tags=["Friends"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(groups.router, prefix="/groups", tags=["Groups"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Chat API!"}
