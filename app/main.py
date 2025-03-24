"""The main entry point of the application."""

from app.api.routes import users, auth, friends, messages, groups, notifications
from app.core.config import settings
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.db.init_db import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio


def create_application() -> FastAPI:
    """Create the FastAPI application."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set up CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Set up event handlers
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    # Run init_db on startup
    application.add_event_handler("startup", lambda: asyncio.create_task(init_db()))
    
    # Include the routers
    application.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
    application.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
    application.include_router(friends.router, prefix=f"{settings.API_V1_STR}/friends", tags=["Friends"])
    application.include_router(messages.router, prefix=f"{settings.API_V1_STR}/messages", tags=["Messages"])
    application.include_router(groups.router, prefix=f"{settings.API_V1_STR}/groups", tags=["Groups"])
    application.include_router(notifications.router, prefix=f"{settings.API_V1_STR}/notifications", tags=["Notifications"])

    return application

app = create_application()

# This allows running the application using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
