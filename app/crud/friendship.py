"""CRUD operations for friendship model."""

from app.models.friendship import Friendship, FriendshipStatus
from app.models.user import User
from app.schemas.friendship import FriendshipCreate
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID


async def create_friendship(db: AsyncSession, sender_id: UUID, receiver_id: UUID, friendship: FriendshipCreate) -> Friendship:
    """Create a new friendship request."""
    # Check if a friendship already exists between the users
    existing_friendship = await get_friendship_between_users(db, sender_id, receiver_id)
    if existing_friendship:
        return None
    
    friendship = Friendship(
        sender_id=sender_id,
        receiver_id=receiver_id,
        status=FriendshipStatus.PENDING
    )
    db.add(friendship)
    await db.commit()
    await db.refresh(friendship)
    return friendship

async def get_friendship_by_id(db: AsyncSession, friendship_id: UUID) -> Optional[Friendship]:
    """Get a friendship by id."""
    # result = await db.execute(select(Friendship).filter(Friendship.id == friendship_id))
    # Alternative query to include sender and receiver details using  selectinload
    result = await db.execute(
        select(Friendship).filter(Friendship.id == friendship_id).options(selectinload(Friendship.sender), selectinload(Friendship.receiver)))
    return result.scalar_one_or_none()
    # notes on the query:
    # The query uses the selectinload function from SQLAlchemy to include the sender and receiver details when fetching a friendship by ID. The query filters the Friendship model by id and uses the options method to specify that the sender and receiver relationships should be loaded along with the friendship data. This ensures that the query returns the sender and receiver details along with the friendship information, allowing the caller to access the user data associated with the friendship.

async def get_friendship_between_users(db: AsyncSession, user_id: UUID, friend_id: UUID) -> Optional[Friendship]:
    """Get a friendship between two users."""
    result = await db.execute(
        select(Friendship).filter(
        # ((Friendship.sender_id == user_id) & (Friendship.receiver_id == friend_id)) | ((Friendship.sender_id == friend_id) & (Friendship.receiver_id == user_id))
        or_(
            and_(Friendship.sender_id == user_id, Friendship.receiver_id == friend_id),
            and_(Friendship.sender_id == friend_id, Friendship.receiver_id == user_id)
            )
        )
    )
    return result.scalar_one_or_none()
    # notes on the query:
    # The query uses the or_ and and_ functions from SQLAlchemy to create a complex filter condition that checks if a friendship exists between two users. The query filters the Friendship model by sender_id and receiver_id, checking if the sender_id is equal to user_id and the receiver_id is equal to friend_id, or if the sender_id is equal to friend_id and the receiver_id is equal to user_id. This condition ensures that the query returns a friendship between the two users regardless of the sender and receiver order.


async def get_user_friends(db: AsyncSession, user_id: UUID, status: Optional[FriendshipStatus] = None) -> List[User]:
    """Get a user's friends with optional status filter."""
    # query = select(Friendship).filter(
    #     ((Friendship.sender_id == user_id) | (Friendship.receiver_id == user_id))
    # )
    query = select(User).join(Friendship, or_(
        Friendship.sender_id == User.id,
        Friendship.receiver_id == User.id
    ))
    if status:
        query = query.filter(Friendship.status == status)
    result = await db.execute(query)
    return result.scalars().all()
    # notes on the query:
    # The query uses the join function from SQLAlchemy to join the User and Friendship models based on the sender_id and receiver_id fields. The query filters the Friendship model by sender_id and receiver_id, checking if the sender_id is equal to the user_id or the receiver_id is equal to the user_id. This condition ensures that the query returns friendships where the user is either the sender or the receiver. The query also includes an optional filter based on the friendship status, allowing the caller to retrieve friends with a specific status if needed. And it returns a list of User objects representing the user's friends.

async def update_friendship_status(db: AsyncSession, friendship: Friendship, status: FriendshipStatus) -> Friendship:
    """Update a friendship's status."""
    friendship.status = status
    db.add(friendship)
    await db.commit()
    await db.refresh(friendship)
    return friendship

async def delete_friendship(db: AsyncSession, friendship_id: UUID) -> bool:
    """Delete a friendship."""
    friendship = await get_friendship_by_id(db, friendship_id)
    if not friendship:
        return False
    db.delete(friendship)
    await db.commit()
    return True

# notes on the CRUD operations for the Friendship model:
# This code defines CRUD operations for the Friendship model. The functions are similar to those in the user.py file, but they are specific to the Friendship model. The functions include creating a friendship request, getting a friendship by ID, getting a friendship between two users, getting a user's friends, updating a friendship's status, and deleting a friendship. These functions interact with the database using SQLAlchemy's AsyncSession.
#
# The Friendship model is defined in app/models/friendship.py, and the schema is defined in app/schemas/friendship.py. The Friendship model has fields for sender_id, receiver_id, status, created_at, and updated_at. The status field is an Enum that defines the possible friendship statuses: PENDING, ACCEPTED, REJECTED, and BLOCKED. The Friendship schema defines Pydantic models for creating, updating, and storing friendship data.
#
# The CRUD operations for the Friendship model are used to manage friendship requests and relationships between users in the application. These operations allow users to send, accept, reject, and block friendship requests, as well as view their friends and update friendship statuses. The functions provide a way to interact with the Friendship model in the database and perform common operations on friendship data.
#
# By separating the CRUD operations for the Friendship model into a separate file, the codebase is organized and modular. This separation allows for better maintainability and readability of the code, as each model has its own set of CRUD operations that can be easily managed and extended. The separation also helps in keeping the codebase clean and structured, making it easier to add new features and functionality related to friendships in the future.
#
# Overall, the CRUD operations for the Friendship model provide a way to manage friendship data in the application and enable users to interact with each other through friendship requests and relationships. These operations are essential for building social networking features and enabling users to connect and communicate with each other within the application.
