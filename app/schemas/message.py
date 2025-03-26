""" """
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class AttachmentBase(BaseModel):
    """Base class for attachment."""
    file_name: str
    file_url: str
    file_type: str
    # size: int

class AttachmentCreate(AttachmentBase):
    """Create attachment class."""
    pass

class AttachmentInDBBase(AttachmentBase):
    """Base class for attachment stored in database."""
    id: str
    message_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Config class for ORM model."""
        orm_mode = True

class Attachment(AttachmentInDBBase):
    """This extends the AttachmentInDBBase fields."""
    pass

class MessageBase(BaseModel):
    """Base class for message."""
    content: str
    is_read: Optional[bool] = False
    is_edited: Optional[bool] = False
    reply_to_message_id: Optional[str] = None

class MessageCreate(MessageBase):
    """Create message class."""
    receiver_id: Optional[str] = None
    group_id: Optional[str] = None
    attachments: Optional[List[AttachmentCreate]] = []

class MessageUpdate(BaseModel):
    """Update message class."""
    content: Optional[str] = None
    is_read: Optional[bool] = None
    is_edited: Optional[bool] = None
    reply_to_message_id: Optional[str] = None

class MessageInDBBase(MessageBase):
    """Base class for message stored in database."""
    id: str
    sender_id: str
    receiver_id: Optional[str] = None
    group_id: Optional[str] = None
    content: str
    is_read: bool
    is_edited: bool
    reply_to_message_id: Optional[str] = None
    created_at: datetime
    edited_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Config class for ORM model."""
        orm_mode = True

class Message(MessageInDBBase):
    """This extends the MessageInDBBase fields."""
    attachments: List[Attachment] = []
