"""User Table Model."""
from app.db.database import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class User(Base):
    """User table"""
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sent_friend_requests = relationship("Friendship", foreign_keys="Friendship.sender_id",back_populates="sender")
    received_friend_requests = relationship("Friendship", foreign_keys="Friendship.receiver_id",back_populates="receiver")
    friends = relationship("Friendship", foreign_keys="Friendship.friend_id",back_populates="friend")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id",back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id",back_populates="receiver")
    notifications = relationship("Notification", back_populates="user")
    created_groups = relationship("Group", foreign_keys="Group.creator_id", back_populates="creator")

    # Many to Many Relationship with groups
    groups = relationship("GroupMember", back_populates="user")
