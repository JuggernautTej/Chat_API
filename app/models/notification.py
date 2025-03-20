"""This houses the models for defining the notification table."""

from app.db.database import Base
from sqlalchemy import Boolean, Column, Enum, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid


class NotificationType(enum.Enum):
    """This class defines the acceptable notification types for the notification table."""
    FRIEND_REQUEST = "friend_request"
    FRIEND_ACCEPTED = "friend_accepted"
    MESSAGE = "message"
    GROUP_INVITATION = "group_invitation"
    GROUP_MESSAGE = "group_message"

class Notification(Base):
    """The notification model defines the structure of the 'notifications' table,
    which stores user notifications for the chat app."""
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="SET NULL"), nullable=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    friendship_id = Column(UUID(as_uuid=True), ForeignKey("friendships.id", ondelete="SET NULL"), nullable=True)
    type = Column(Enum(NotificationType), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    sender = relationship("User", foreign_keys=[sender_id])
    group = relationship("Group", foreign_keys=[group_id])
    message = relationship("Message", foreign_keys=[message_id])
    friendship = relationship("Friendship", foreign_keys=[friendship_id])

# to do - add an expiration mechanis to auto-delete notifications after a certain period of time
# to do - add a method to mark notifications as read
