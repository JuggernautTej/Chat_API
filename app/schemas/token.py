"""Script that defines the structure of a token."""

from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """This represents the structure of a token."""
    access_token: str
    token_type: str
    # expires_in: int
    # refresh_token: Optional[str] = None
    # scope: Optional[str] = None

class TokenPayload(BaseModel):
    """This decodes the payload of the token."""
    sub: Optional[str] = None
    # exp: Optional[datetime] = None
    # username: Optional[str] = None
    # scope: Optional[str] = None
    # token_type: Optional[str] = None
    # user_id: Optional[str] = None
    # is_active: Optional[bool] = None
    # is_online: Optional[bool] = None
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # email: Optional[str] = None
    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None
