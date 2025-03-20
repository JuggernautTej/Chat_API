"""The message model"""

from app.db.database import Base
from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Message(Base):
    """The message model defines the structure of the 'messages' table, 
    which stores user messages for a messaging app."""
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=True)
    content = Column(Text, nullable=False)
    attachment_id = Column(UUID(as_uuid=True), ForeignKey("attachments.id", ondelete="SET NULL"), nullable=True)
    is_read = Column(Boolean, default=False)
    is_edited = Column(Boolean, default=False)
    reply_to_message_id = Column(String, ForeignKey("messages.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    group = relationship("Group", back_populates="messages")
    reply_to = relationship("Message",remote_side="Message.id", back_populates="replies")
    attachments = relationship("Attachment", back_populates="message", uselist=True)
    replies = relationship("Message", back_populates="reply_to", uselist=True)

    # Define either receiver_id or group_id must be set, but not both
    __table_args__ = (
        # Check constaint: one of receiver_id or group_id must be not be null
        CheckConstraint('NOT(receiver_id IS NULL AND group_id IS NULL)'),
        # Check constraint: both receiver_id and group_id cannot be null
        CheckConstraint('NOT(receiver_id IS NOT NULL AND group_id IS NOT NULL)'),
    )

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"))
    file_url = Column(String, nullable=False)
    file_name = Column(String, nullable=True)
    file_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    message = relationship("Message", back_populates="attachments")

# to do - implement message reactions
# to do - implement message editing and deletion
# to do - implement read receipts per user for group chats
# to do - implement message search
