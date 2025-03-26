"""Friendship schema module."""
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional


class FriendshipStatus(str, Enum):
    """This defines friendship statuses."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"

class FriendshipBase(BaseModel):
    """This class defines the shared properties for a friendship."""
    sender_id: UUID4
    receiver_id: UUID4
    status: Optional[FriendshipStatus] = FriendshipStatus.PENDING

class FriendshipCreate(FriendshipBase):
    """Friendship create class."""
    receiver_id: UUID4

class FriendshipUpdate(FriendshipBase):
    """This class updates the friendship status."""
    status: FriendshipStatus

class FriendshipInDBBase(FriendshipBase):
    """This class is used in storing friendship data in the database."""
    id: UUID4
    sender_id: UUID4
    receiver_id: UUID4
    status: FriendshipStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Config class for ORM model."""
        orm_mode = True

class Friendship(FriendshipInDBBase):
    """This extends the FriendshipInDBBase fields."""
    pass
