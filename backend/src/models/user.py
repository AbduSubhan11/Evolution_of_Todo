from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from pydantic import field_validator
from pydantic.networks import EmailStr

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    is_active: bool = Field(default=True, index=True)

class User(UserBase, table=True):
    """
    User model representing a registered user in the system with authentication capabilities
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

class UserCreate(UserBase):
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None