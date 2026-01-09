from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from pydantic import field_validator

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending", index=True)  # pending, completed, archived
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)

class Task(TaskBase, table=True):
    """
    Task model representing a todo item that belongs to a specific authenticated user
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    completed_at: Optional[datetime] = Field(index=True, default=None)

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"

    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title is required and cannot be empty')
        if len(v) > 255:
            raise ValueError('Title must be 255 characters or less')
        return v.strip()

    @field_validator('status')
    def validate_status(cls, v):
        if v and v not in ["pending", "completed", "archived"]:
            raise ValueError('Status must be one of: pending, completed, archived')
        return v

class TaskRead(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # pending, completed, archived

    @field_validator('title', mode='before')
    def validate_title(cls, v):
        if v is not None:
            if not v or len(v.strip()) == 0:
                raise ValueError('Title is required and cannot be empty')
            if len(v) > 255:
                raise ValueError('Title must be 255 characters or less')
            return v.strip()
        return v

    @field_validator('status', mode='before')
    def validate_status(cls, v):
        if v is not None and v not in ["pending", "completed", "archived"]:
            raise ValueError('Status must be one of: pending, completed, archived')
        return v