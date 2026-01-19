from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel


# SQLModel for Conversations
class ConversationBase(SQLModel):
    user_id: UUID = Field(foreign_key="auth.users.id")
    metadata: Optional[dict] = Field(default={})


class Conversation(ConversationBase, table=True):
    conversation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


# SQLModel for Messages
class MessageBase(SQLModel):
    conversation_id: UUID = Field(foreign_key="conversation.conversation_id")
    sender_type: str = Field(regex="^(user|ai)$")  # 'user' or 'ai'
    role: str = Field(regex="^(user|assistant|tool)$")  # 'user', 'assistant', or 'tool'
    content: str = Field(max_length=10000)
    tool_calls: Optional[dict] = Field(default={})


class Message(MessageBase, table=True):
    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")


# SQLModel for Task Operation Logs
class TaskOperationLogBase(SQLModel):
    conversation_id: UUID = Field(foreign_key="conversation.conversation_id")
    user_message_id: UUID = Field(foreign_key="message.message_id")
    operation_type: str = Field(regex="^(add|list|complete|delete|update)$")
    input_params: Optional[dict] = Field(default=None)
    result: Optional[dict] = Field(default=None)
    status: str = Field(regex="^(pending|success|failed)$", default="pending")


class TaskOperationLog(TaskOperationLogBase, table=True):
    operation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Pydantic models for API requests/responses
class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    conversation_id: UUID
    created_at: datetime
    updated_at: datetime


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    message_id: UUID
    timestamp: datetime


class TaskOperationLogCreate(TaskOperationLogBase):
    pass


class TaskOperationLogRead(TaskOperationLogBase):
    operation_id: UUID
    timestamp: datetime