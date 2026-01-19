import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.agents.chat_agent import initialize_chat_agent, process_user_message


@pytest.mark.asyncio
async def test_initialize_chat_agent():
    """Test that initialize_chat_agent creates an assistant correctly"""
    user_id = uuid4()

    with patch('core.tools.task_tools.get_task_tools_for_user') as mock_get_tools, \
         patch('utils.ai_client.ai_client.create_assistant') as mock_create_assistant:

        # Mock return values
        mock_get_tools.return_value = [{"type": "function", "function": {"name": "test_tool"}}]
        mock_create_assistant.return_value = "test-assistant-id"

        result = await initialize_chat_agent(user_id)

        # Verify the result
        assert result == "test-assistant-id"

        # Verify the calls were made correctly
        mock_get_tools.assert_called_once_with(str(user_id))
        mock_create_assistant.assert_called_once()

        # Verify that the call to create_assistant had the correct parameters
        call_args = mock_create_assistant.call_args
        assert "instructions" in call_args.kwargs
        assert "tools" in call_args.kwargs
        assert str(user_id) in call_args.kwargs["instructions"]


@pytest.mark.asyncio
async def test_process_user_message():
    """Test that process_user_message works correctly"""
    user_id = uuid4()
    conversation_id = str(uuid4())
    message = "Test message"

    with patch('core.agents.chat_agent.initialize_chat_agent') as mock_init_agent, \
         patch('utils.ai_client.ai_client.run_assistant') as mock_run_assistant:

        # Mock return values
        mock_init_agent.return_value = "test-assistant-id"

        # Mock AIResponse
        mock_response = MagicMock()
        mock_response.content = "Test response content"
        mock_response.tool_calls = [{"id": "call1", "function": {"name": "test_func"}}]
        mock_run_assistant.return_value = mock_response

        result = await process_user_message(user_id, conversation_id, message)

        # Verify the result
        assert "response" in result
        assert "tool_calls" in result
        assert "conversation_id" in result
        assert result["response"] == "Test response content"
        assert result["conversation_id"] == conversation_id

        # Verify the calls were made correctly
        mock_init_agent.assert_called_once_with(user_id)
        mock_run_assistant.assert_called_once_with(conversation_id, "test-assistant-id")


@pytest.mark.asyncio
async def test_initialize_chat_agent_with_error():
    """Test that initialize_chat_agent handles errors correctly"""
    user_id = uuid4()

    with patch('core.tools.task_tools.get_task_tools_for_user') as mock_get_tools:
        mock_get_tools.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            await initialize_chat_agent(user_id)


@pytest.mark.asyncio
async def test_process_user_message_with_error():
    """Test that process_user_message handles errors correctly"""
    user_id = uuid4()
    conversation_id = str(uuid4())
    message = "Test message"

    with patch('core.agents.chat_agent.initialize_chat_agent') as mock_init_agent:
        mock_init_agent.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            await process_user_message(user_id, conversation_id, message)