from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID
from ..models.chat_models import Conversation, Message, TaskOperationLog
from ..models.user import User
from datetime import datetime


class ChatRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: UUID, metadata: Optional[dict] = None) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            metadata=metadata or {}
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by ID."""
        statement = select(Conversation).where(Conversation.conversation_id == conversation_id)
        return self.session.exec(statement).first()

    def get_conversations_by_user(self, user_id: UUID) -> List[Conversation]:
        """Get all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return self.session.exec(statement).all()

    def create_message(self, conversation_id: UUID, sender_type: str, role: str, content: str, tool_calls: Optional[dict] = None) -> Message:
        """Create a new message in a conversation."""
        message = Message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            role=role,
            content=content,
            tool_calls=tool_calls or {}
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_messages_by_conversation(self, conversation_id: UUID, limit: int = 50, offset: int = 0) -> List[Message]:
        """Get messages for a conversation with pagination."""
        statement = select(Message).where(Message.conversation_id == conversation_id).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def create_task_operation_log(self, conversation_id: UUID, user_message_id: UUID, operation_type: str, input_params: Optional[dict] = None, result: Optional[dict] = None) -> TaskOperationLog:
        """Create a task operation log entry."""
        operation_log = TaskOperationLog(
            conversation_id=conversation_id,
            user_message_id=user_message_id,
            operation_type=operation_type,
            input_params=input_params,
            result=result,
            status="pending"
        )
        self.session.add(operation_log)
        self.session.commit()
        self.session.refresh(operation_log)
        return operation_log

    def update_task_operation_log_status(self, operation_id: UUID, status: str, result: Optional[dict] = None) -> Optional[TaskOperationLog]:
        """Update the status of a task operation log."""
        operation_log = self.session.get(TaskOperationLog, operation_id)
        if operation_log:
            operation_log.status = status
            if result:
                operation_log.result = result
            self.session.add(operation_log)
            self.session.commit()
            self.session.refresh(operation_log)
        return operation_log

    def get_task_operation_logs_by_conversation(self, conversation_id: UUID) -> List[TaskOperationLog]:
        """Get all task operation logs for a conversation."""
        statement = select(TaskOperationLog).where(TaskOperationLog.conversation_id == conversation_id)
        return self.session.exec(statement).all()