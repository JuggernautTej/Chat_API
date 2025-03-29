"""CRUD operations for the messages model."""

from app.models.messages import Message, Attachment
from app.schemas.message import MessageCreate, AttachmentCreate
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

async def create_message(db: AsyncSession, message: MessageCreate, sender_id: UUID) -> Message:
    """Create a new message."""

    if not message.receiver_id and not message.group_id:
        raise ValueError("Either receiver_id or group_id must be provided.")

    # Preparing attachments
    attachments = []
    if message.attachments:
        attachments = [
            Attachment(
                **AttachmentCreate(**attachment.model_dump()).model_dump(exclude_unset=True)
            ) for attachment in message.attachments
        ]
    
    # Create message
    message = Message(
        sender_id=sender_id,
        receiver_id=message.receiver_id,
        group_id=message.group_id,
        content=message.content,
        reply_to_message_id=message.reply_to_message_id,
        is_read=False,
        attachments=attachments
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message

async def get_message_by_id(db: AsyncSession, message_id: UUID) -> Optional[Message]:
    """Get a message by id."""
    result = await db.execute(select(Message).filter(Message.id == message_id))
    return result.scalar_one_or_none()

async def get_conversation_messages(
        db: AsyncSession,
        user_id: UUID,
        other_user_id: UUID,
        skip: int = 0,
        limit: int = 100
        ) -> List[Message]:
    """Get messages between two users."""
    result = await db.execute(
        select(Message)
        .filter(
            or_(
                and_(Message.sender_id == user_id, Message.receiver_id == other_user_id),
                and_(Message.sender_id == other_user_id, Message.receiver_id == user_id)
            )
        )
        .order_by(Message.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_group_messages(db: AsyncSession, group_id: UUID, skip: int = 0, limit: int = 100) -> List[Message]:
    """Get messages in a group."""
    result = await db.execute(
        select(Message).filter(Message.group_id == group_id).order_by(Message.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_message(db: AsyncSession, message_id: UUID, message_in: Union[MessageCreate, Dict[str, Any]]) -> Optional[Message]:
    """Update an existing message."""
    message = await get_message_by_id(db, message_id)
    if not message:
        return None
    
    # Convert input to dictionary if it's a Pydantic model
    if not isinstance(message_in, dict):
        message_in = message_in.model_dump(exclude_unset=True)
    
    # Update message fields
    for key, value in message_in.items():
        setattr(message, key, value)
    
    await db.commit()
    await db.refresh(message)
    return message

async def delete_message(db: AsyncSession, message_id: UUID) -> Optional[Message]:
    """Delete a message."""
    message = await get_message_by_id(db, message_id)
    if not message:
        return {"error": "Message not found"}
    await db.delete(message)
    await db.commit()
    return {"message": "Message deleted successfully"}

async def mark_message_as_read(db: AsyncSession, message_id: UUID) -> Optional[Message]:
    """Mark a message as read."""
    message = await get_message_by_id(db, message_id)
    if not message:
        return None
    message.is_read = True
    await db.commit()
    await db.refresh(message)
    return message
# Code summary:
# This snippet defines CRUD operations for the messages model. The create_message function creates a new message in the database, including any attachments associated with the message. The get_message_by_id function retrieves a message by its ID. The get_conversation_messages function retrieves messages exchanged between two users. The get_group_messages function retrieves messages in a group. The update_message function updates an existing message. The delete_message function deletes a message. The mark_message_as_read function marks a message as read in the database.
#
# The CRUD operations for the messages model provide the necessary functionality to manage messages in the messaging application. These operations allow users to create, retrieve, update, and delete messages, as well as mark messages as read. By implementing these operations, the application can handle message-related interactions between users and groups effectively.
#
# The CRUD operations for the messages model provide the necessary functionality to manage messages in the messaging application. These operations allow users to create, retrieve, update, and delete messages, as well as mark messages as read. By implementing these operations, the application can handle message-related interactions between users and groups effectively.
#
