# Data Model: Todo AI Chatbot

**Feature**: Todo AI Chatbot
**Date**: 2026-01-17

## Entity Relationships

### Conversation
- **conversation_id** (UUID, Primary Key)
  - Unique identifier for each conversation thread
- **user_id** (UUID, Foreign Key to users table)
  - Links conversation to authenticated user
- **created_at** (TIMESTAMPTZ)
  - Timestamp when conversation started
- **updated_at** (TIMESTAMPTZ)
  - Timestamp of last activity in conversation
- **metadata** (JSONB)
  - Additional conversation context (status, settings, etc.)

### Message
- **message_id** (UUID, Primary Key)
  - Unique identifier for each message
- **conversation_id** (UUID, Foreign Key to conversations)
  - Links message to parent conversation
- **sender_type** (ENUM: 'user', 'ai')
  - Identifies who sent the message
- **content** (TEXT)
  - The actual message content
- **timestamp** (TIMESTAMPTZ)
  - When the message was created
- **tool_calls** (JSONB)
  - Details of any tools called during this message
- **role** (VARCHAR)
  - Role in conversation ('user', 'assistant', 'tool')

### TaskOperationLog
- **operation_id** (UUID, Primary Key)
  - Unique identifier for each operation
- **conversation_id** (UUID, Foreign Key to conversations)
  - Links operation to conversation
- **user_message_id** (UUID, Foreign Key to messages)
  - Reference to the user message that triggered the operation
- **operation_type** (ENUM: 'add', 'list', 'complete', 'delete', 'update')
  - Type of task operation performed
- **input_params** (JSONB)
  - Parameters provided to the operation
- **result** (JSONB)
  - Result of the operation
- **status** (ENUM: 'pending', 'success', 'failed')
  - Status of the operation
- **timestamp** (TIMESTAMPTZ)
  - When the operation was executed

## Database Schema

```sql
-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    metadata JSONB DEFAULT '{}',
    INDEX idx_conversations_user_id (user_id),
    INDEX idx_conversations_updated_at (updated_at)
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE NOT NULL,
    sender_type VARCHAR(10) CHECK (sender_type IN ('user', 'ai')) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    tool_calls JSONB DEFAULT '{}',
    INDEX idx_messages_conversation_id (conversation_id),
    INDEX idx_messages_timestamp (timestamp)
);

-- Task operation logs table
CREATE TABLE IF NOT EXISTS task_operation_logs (
    operation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE NOT NULL,
    user_message_id UUID REFERENCES messages(message_id) ON DELETE CASCADE NOT NULL,
    operation_type VARCHAR(20) CHECK (operation_type IN ('add', 'list', 'complete', 'delete', 'update')) NOT NULL,
    input_params JSONB,
    result JSONB,
    status VARCHAR(20) CHECK (status IN ('pending', 'success', 'failed')) DEFAULT 'pending',
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    INDEX idx_task_operations_conversation_id (conversation_id),
    INDEX idx_task_operations_status (status)
);
```

## Validation Rules

### Conversation
- Must have valid user_id that exists in users table
- Cannot have more than 1000 messages per conversation (to prevent performance issues)
- Metadata must be valid JSON

### Message
- Content length limited to 10,000 characters
- Sender_type must be either 'user' or 'ai'
- Role must be one of 'user', 'assistant', or 'tool'
- Must belong to an existing conversation

### TaskOperationLog
- Operation type must be one of the allowed values
- Status must be one of the allowed values
- Must reference valid conversation and message IDs
- Input params and result must be valid JSON

## State Transitions

### Conversation States
- Active → Archived (after 90 days of inactivity)
- Active → Deleted (when user deletes conversation)

### TaskOperationLog States
- pending → success (when operation completes successfully)
- pending → failed (when operation encounters an error)