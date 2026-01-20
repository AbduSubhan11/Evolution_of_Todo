import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import UUID, uuid4
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app  # Adjust import based on your main app location

client = TestClient(app)


@pytest.mark.asyncio
async def test_full_chat_flow():
    """
    Test the complete flow: user sends message -> AI processes -> tools are called -> response returned
    """
    user_id = str(uuid4())

    with patch('src.api.v1.endpoints.chat.initialize_chat_agent') as mock_init_agent, \
         patch('utils.ai_client.ai_client.create_thread') as mock_create_thread, \
         patch('utils.ai_client.ai_client.add_message_to_thread') as mock_add_msg, \
         patch('utils.ai_client.ai_client.run_assistant') as mock_run_assistant:

        # Mock the assistant initialization
        mock_init_agent.return_value = "test-assistant-id"
        mock_create_thread.return_value = "test-thread-id"

        # Mock the AI response with tool calls
        mock_response = MagicMock()
        mock_response.content = "I've added your task."
        mock_response.tool_calls = [
            {
                "id": "call_abc123",
                "function": {
                    "name": "add_task",
                    "arguments": '{"title": "Buy groceries", "description": "Milk, bread, eggs"}'
                },
                "type": "function"
            }
        ]
        mock_run_assistant.return_value = mock_response

        # Make the request
        response = client.post(
            f"/api/{user_id}/chat",
            json={
                "message": "Add a task to buy groceries: milk, bread, and eggs"
            },
            headers={
                "Authorization": "Bearer test-token"
            }
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["response"] == "I've added your task."
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["function"]["name"] == "add_task"
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_chat_flow_with_list_tasks():
    """
    Test the flow when user asks to list tasks
    """
    user_id = str(uuid4())

    with patch('src.api.v1.endpoints.chat.initialize_chat_agent') as mock_init_agent, \
         patch('utils.ai_client.ai_client.create_thread') as mock_create_thread, \
         patch('utils.ai_client.ai_client.add_message_to_thread') as mock_add_msg, \
         patch('utils.ai_client.ai_client.run_assistant') as mock_run_assistant:

        # Mock the assistant initialization
        mock_init_agent.return_value = "test-assistant-id"
        mock_create_thread.return_value = "test-thread-id"

        # Mock the AI response with list_tasks tool call
        mock_response = MagicMock()
        mock_response.content = "Here are your tasks:"
        mock_response.tool_calls = [
            {
                "id": "call_def456",
                "function": {
                    "name": "list_tasks",
                    "arguments": '{"status_filter": "pending"}'
                },
                "type": "function"
            }
        ]
        mock_run_assistant.return_value = mock_response

        # Make the request
        response = client.post(
            f"/api/{user_id}/chat",
            json={
                "message": "Show me my pending tasks"
            },
            headers={
                "Authorization": "Bearer test-token"
            }
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["response"] == "Here are your tasks:"
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["function"]["name"] == "list_tasks"


@pytest.mark.asyncio
async def test_chat_flow_with_multiple_tool_calls():
    """
    Test the flow when multiple tools are called in one response
    """
    user_id = str(uuid4())

    with patch('src.api.v1.endpoints.chat.initialize_chat_agent') as mock_init_agent, \
         patch('utils.ai_client.ai_client.create_thread') as mock_create_thread, \
         patch('utils.ai_client.ai_client.add_message_to_thread') as mock_add_msg, \
         patch('utils.ai_client.ai_client.run_assistant') as mock_run_assistant:

        # Mock the assistant initialization
        mock_init_agent.return_value = "test-assistant-id"
        mock_create_thread.return_value = "test-thread-id"

        # Mock the AI response with multiple tool calls
        mock_response = MagicMock()
        mock_response.content = "I've completed your task and added a new one."
        mock_response.tool_calls = [
            {
                "id": "call_1",
                "function": {
                    "name": "complete_task",
                    "arguments": '{"task_id": "some-task-id"}'
                },
                "type": "function"
            },
            {
                "id": "call_2",
                "function": {
                    "name": "add_task",
                    "arguments": '{"title": "Follow up tomorrow"}'
                },
                "type": "function"
            }
        ]
        mock_run_assistant.return_value = mock_response

        # Make the request
        response = client.post(
            f"/api/{user_id}/chat",
            json={
                "message": "Complete the meeting task and add follow up for tomorrow"
            },
            headers={
                "Authorization": "Bearer test-token"
            }
        )

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["response"] == "I've completed your task and added a new one."
        assert len(data["tool_calls"]) == 2
        tool_names = [tc["function"]["name"] for tc in data["tool_calls"]]
        assert "complete_task" in tool_names
        assert "add_task" in tool_names


def test_api_endpoint_validation():
    """
    Test that the API endpoint properly validates input
    """
    user_id = str(uuid4())

    # Test with missing message
    response = client.post(
        f"/api/{user_id}/chat",
        json={},
        headers={
            "Authorization": "Bearer test-token"
        }
    )

    # Should return validation error
    assert response.status_code == 422

    # Test with empty message
    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "message": ""
        },
        headers={
            "Authorization": "Bearer test-token"
        }
    )

    # Should return 200 (validation happens in the AI agent)
    assert response.status_code in [200, 400]


@pytest.mark.asyncio
async def test_conversation_persistence():
    """
    Test that conversation ID is properly maintained across requests
    """
    user_id = str(uuid4())
    conversation_id = "test-conversation-id"

    with patch('src.api.v1.endpoints.chat.initialize_chat_agent') as mock_init_agent, \
         patch('utils.ai_client.ai_client.add_message_to_thread') as mock_add_msg, \
         patch('utils.ai_client.ai_client.run_assistant') as mock_run_assistant:

        # Mock the assistant initialization
        mock_init_agent.return_value = "test-assistant-id"

        # Mock the AI response
        mock_response = MagicMock()
        mock_response.content = "Got your message for the existing conversation."
        mock_response.tool_calls = []
        mock_run_assistant.return_value = mock_response

        # Make the request with existing conversation ID
        response = client.post(
            f"/api/{user_id}/chat",
            json={
                "conversation_id": conversation_id,
                "message": "Continue our conversation about the project"
            },
            headers={
                "Authorization": "Bearer test-token"
            }
        )

        # Verify the response includes the same conversation ID
        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == conversation_id  # Should return the same ID