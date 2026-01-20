-- Migration: Create chat tables for AI chatbot feature
-- Description: Creates conversations, messages, and task_operation_logs tables

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    metadata JSONB DEFAULT '{}'
);

-- Create index on conversations for user_id
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);

-- Create index on conversations for updated_at
CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE NOT NULL,
    sender_type VARCHAR(10) CHECK (sender_type IN ('user', 'ai')) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    tool_calls JSONB DEFAULT '{}'
);

-- Create index on messages for conversation_id
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);

-- Create index on messages for timestamp
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);

-- Create task operation logs table
CREATE TABLE IF NOT EXISTS task_operation_logs (
    operation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE NOT NULL,
    user_message_id UUID REFERENCES messages(message_id) ON DELETE CASCADE NOT NULL,
    operation_type VARCHAR(20) CHECK (operation_type IN ('add', 'list', 'complete', 'delete', 'update')) NOT NULL,
    input_params JSONB,
    result JSONB,
    status VARCHAR(20) CHECK (status IN ('pending', 'success', 'failed')) DEFAULT 'pending',
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Create index on task_operation_logs for conversation_id
CREATE INDEX IF NOT EXISTS idx_task_operations_conversation_id ON task_operation_logs(conversation_id);

-- Create index on task_operation_logs for status
CREATE INDEX IF NOT EXISTS idx_task_operations_status ON task_operation_logs(status);