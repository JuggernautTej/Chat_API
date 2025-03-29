"""CRUD operations for notifications model."""

from app.models.notification import Notification, NotificationType
from app.schemas.notification import NotificationCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID


async def create_notification(db: AsyncSession, notification: NotificationCreate) -> Notification:
    """Create a new notification."""
    # Ensure at least one of the optional fields is provided
    if not any([
        notification.sender_id,
        notification.group_id,
        notification.message_id,
        notification.friendship_id
    ]):
        raise ValueError("At least one of sender_id, group_id, message_id, or friendship_id must be provided.")
     
    # Check if the notification type is valid
    if notification.type not in NotificationType:
        raise ValueError("Invalid notification type.")
    

    db_notification = Notification(
        user_id=notification.user_id,
        sender_id=notification.sender_id,
        group_id=notification.group_id,
        type=notification.type,
        message_id=notification.message_id,
        friendship_id=notification.friendship_id,
        message=notification.content,
        is_read=False,
    )
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification

async def get_user_notifications(
    db: AsyncSession,
    user_id: UUID,
    is_read: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Notification]:
    """Get notifications for a user."""
    query = select(Notification).filter(Notification.user_id == user_id)
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    result = await db.execute(
        query.order_by(Notification.created_at.desc())
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

async def mark_notification_as_read(db: AsyncSession, notification_id: UUID) -> Optional[Notification]:
    """Mark a notification as read."""
    result = await db.execute(
        select(Notification).filter(Notification.id == notification_id)
        )
    notification = result.scalar_one_or_none()
    if notification:
        notification.is_read = True
        await db.commit()
        await db.refresh(notification)
    return notification

async def delete_notification(db: AsyncSession, notification_id: UUID) -> Optional[Notification]:
    """Delete a notification."""
    result = await db.execute(
        select(Notification).filter(Notification.id == notification_id)
        )
    notification = result.scalar_one_or_none()
    if notification:
        await db.delete(notification)
        await db.commit()
    return notification
# Code Summary:
# This code provides CRUD operations for managing notifications in a database using SQLAlchemy. It includes functions to create, retrieve, update, and delete notifications. The notifications can be filtered by user ID and read status. The code uses asynchronous database operations with SQLAlchemy's AsyncSession.
# The `Notification` model is used to represent the notification data, and the `NotificationCreate` schema is used for creating new notifications. The code also includes type hints for better readability and maintainability.
# Overall, this code is part of a larger application that likely involves user notifications in a chat or messaging system.
# The operations are designed to be efficient and scalable, allowing for pagination of results when retrieving notifications.
# The use of async functions allows for non-blocking database interactions, which is beneficial in a web application context where multiple requests may be handled concurrently.
# The code is structured to be easily integrated into a FastAPI application, making it suitable for modern web development practices.
# The functions are designed to be reusable and modular, allowing for easy expansion or modification in the future.
# The code is also designed to handle potential errors gracefully, ensuring that the application can respond appropriately to various scenarios, such as missing notifications or database issues.
# Overall, this code provides a solid foundation for managing notifications in a web application, with a focus on performance and usability.
# To-do:
# - Add more detailed error handling and logging.
# - Implement unit tests for each CRUD operation.
# - Consider adding more filtering options for notifications (e.g., by type).
# - Optimize database queries for better performance.
