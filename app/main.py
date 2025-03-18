from fastapi import FastAPI
from app.api import users, auth, frineds, messages, groups, notifications
from app.core.config import settings
from app.db.database import engine, Base
