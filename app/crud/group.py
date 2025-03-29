"""CRUD operations for the group model."""

from app.models.group import Group, GroupMember
from app.schemas.group import GroupCreate, GroupUpdate
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID


async def create_group(db: AsyncSession, group: GroupCreate, creator_id: UUID) -> Group:
    """Create a new group chat."""
    # Check if the group name already exists
    existing_group = await db.execute(
        select(Group).filter(Group.name == group.name)
    )
    if existing_group.scalar_one_or_none():
        raise ValueError("Group name already exists.")
    
    # Create the group
    db_group = Group(
        name=group.name,
        description=group.description,
        image_url=group.image_url,
        creator_id=creator_id
    )

    # Add the creator as the first member of the group
    creator_member = GroupMember(
        user_id=creator_id,
        group=db_group,
        is_admin=True
    )
    db_group.members.append(creator_member)

    # Ensure unique memebers
    unique_members = set(group.member_id or [])
    unique_members.discard(creator_id)  # Remove creator_id if present

    # Add other unique members to the group
    db_group.members.extend([
        GroupMember(
            user_id=member_id,
            group=db_group,
            is_admin=False
        ) for member_id in unique_members
    ])

    # Add the group to the session and commit
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group

async def get_group_by_id(db: AsyncSession, group_id: UUID) -> Optional[Group]:
    """Get a group by id."""
    result = await db.execute(select(Group).filter(Group.id == group_id))
    return result.scalar_one_or_none()
    # Code notes/to-do:
    # I am not sure if it's necessary to include the members in this query.
    # If you want to include the members, you can use the following query:
    # result = await db.execute(
    #     select(Group).filter(Group.id == group_id).options(selectinload(Group.members)))
    # The same applies for the other get_group_by_* functions.


async def get_group_by_name(db: AsyncSession, group_name: str) -> Optional[Group]:
    """Get a group by name."""
    result = await db.execute(select(Group).filter(Group.name == group_name))
    return result.scalar_one_or_none()

async def update_group(db: AsyncSession, group: Group, group_in: GroupUpdate) -> Group:
    """Update the details of a group."""
    # Check if the group exists
    if not group:
        raise ValueError("Group not found.")
    
    # Update group attributes
    update_data = group_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(group, key, value)
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group

async def add_group_member(db: AsyncSession, group_id: UUID,
                           user_id: UUID, is_admin: bool = False) -> Optional[GroupMember]:
    """Add a user to a group."""
    # Check if the group exists
    group = await get_group_by_id(db, group_id)
    if not group:
        raise ValueError("Group not found.")
    
    # Check if the user is already a member of the group
    existing_member = await db.execute(
        select(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        ))
    if existing_member.scalar_one_or_none():
        raise ValueError("User is already a member of the group.")
    
    # Create a new group member
    new_member = GroupMember(
        group_id=group_id,
        user_id=user_id,
        is_admin=is_admin
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)
    return new_member

async def remove_group_member(db: AsyncSession, group_id: UUID, user_id: UUID) -> Optional[GroupMember]:
    """Remove a user from a group."""
    # Check if the group exists
    group = await get_group_by_id(db, group_id)
    if not group:
        raise ValueError("Group not found.")
    
    # Check if the user is a member of the group
    member_check = await db.execute(
        select(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        ))
    member = member_check.scalar_one_or_none()
    
    if not member:
        raise ValueError("User is not a member of the group.")
    db.delete(member)
    await db.commit()
    return {"message": "User removed from group."}

async def get_group_members(db: AsyncSession, group_id: UUID) -> List[GroupMember]:
    """Get all members of a group."""
    result = await db.execute(
        select(GroupMember).filter(GroupMember.group_id == group_id)
    )
    return result.scalars().all()

async def get_user_groups(db: AsyncSession, user_id: UUID) -> List[Group]:
    """Get all groups a user is a member of."""
    result = await db.execute(
        select(Group).join(GroupMember).filter(GroupMember.user_id == user_id)
    )
    return result.scalars().all()
# Code Summary:
# This code defines CRUD operations for managing group chats in a chat application.
# It includes functions to create, update, and delete groups and group members, as well as to retrieve group information.
# The operations are performed using SQLAlchemy with asynchronous database sessions.
# The code also handles errors such as group name conflicts and membership checks.
# The functions are designed to be used in a FastAPI application, allowing for efficient management of group chats and their members.
# The code is structured to ensure that group members can be added or removed, and that group details can be updated as needed.
# Overall, this code provides a comprehensive set of CRUD operations for group management in a chat application.

# To-do:
# - Add tests for the CRUD operations.
# - Add error handling for database operations.
# - Add pagination for group members and user groups retrieval.
# - Add more detailed docstrings for each function.
