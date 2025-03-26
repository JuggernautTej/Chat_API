""".."""

from enum import Enum
from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional


class NotificationType(str, Enum):
    """This defines notification types."""
    FRIEND_REQUEST = "friend_request"
    FRIEND_ACCEPTED = "friend_accepted"
    MESSAGE = "message"
    GROUP_INVITATION = "group_invitation"
    GROUP_MESSAGE = "group_message"

class NotificationBase(BaseModel):
    """This class defines the shared properties for a notification."""
    type: NotificationType
    content: str
    is_read: Optional[bool] = False

class NotificationCreate(NotificationBase):
    """Notification create class."""
    user_id: UUID4
    sender_id: Optional[UUID4] = None
    group_id: Optional[UUID4] = None
    message_id: Optional[UUID4] = None
    friendship_id: Optional[UUID4] = None

class NotificationUpdate(NotificationBase):
    """This class updates the notification status."""
    is_read: bool

class NotificationInDBBase(NotificationBase):
    """This class is used in storing notification data in the database."""
    id: UUID4
    user_id: UUID4
    sender_id: Optional[UUID4] = None
    group_id: Optional[UUID4] = None
    message_id: Optional[UUID4] = None
    friendship_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Config class for ORM model."""
        orm_mode = True

class Notification(NotificationInDBBase):
    """This extends the NotificationInDBBase fields."""
    pass
