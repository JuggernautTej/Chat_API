""" """

from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional, List

class GroupBase(BaseModel):
    """Base class for group."""
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class GroupCreate(GroupBase):
    """Create group class."""
    member_id: Optional[List[UUID4]] = []

class GroupUpdate(BaseModel):
    """Update group class."""
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class GroupInDBBase(GroupBase):
    """Base class for group stored in database."""
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Config class for ORM model."""
        orm_mode = True

class Group(GroupInDBBase):
    """This extends the GroupInDBBase fields."""
    pass

class GroupMemberBase(BaseModel):
    """Base class for group member."""
    is_admin: Optional[bool] = False

class GroupMemberCreate(GroupMemberBase):
    """Create group member class."""
    user_id: UUID4

class GroupMemberUpdate(BaseModel):
    """Update group member class."""
    is_admin: bool

class GroupMemberInDBBase(GroupMemberBase):
    """Base class for group member stored in database."""
    id: UUID4
    group_id: UUID4
    user_id: UUID4
    is_admin: bool
    joined_at: datetime

    class Config:
        """Config class for ORM model."""
        orm_mode = True

class GroupMember(GroupMemberInDBBase):
    """This extends the GroupMemberInDBBase fields."""
    pass
