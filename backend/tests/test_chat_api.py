import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from uuid import UUID, uuid4
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app  # Adjust import based on your main app location

client = TestClient(app)

@pytest.fixture
def mock_user_id():
    return str(uuid4())

@pytest.mark.asyncio
async def test_chat_endpoint_success(mock_user_id):
    """Test that the chat endpoint works correctly with valid input"""
    # Mock the AI client and agent initialization
    with patch('src.api.v1.endpoints.chat.initialize_chat_agent') as mock_init_agent, \
         patch('utils.ai_client.ai_client.create_thread') as mock_create_thread, \
         patch('utils.ai_client.ai_client.add_message_to_thread') as mock_add_msg, \
         patch('utils.ai_client.ai_client.run_assistant') as mock_run_assistant:

        # Set up mocks
        mock_init_agent.return_value = "test-assistant-id"
        mock_create_thread.return_value = "test-thread-id"
        mock_run_assistant.return_value = AsyncMock()
        mock_run_assistant.return_value.content = "Test response"
        mock_run_assistant.return_value.tool_calls = []

        # Make request
        response = client.post(
            f"/api/{mock_user_id}/chat",
            json={
                "message": "Add a test task"
            },
            headers={
                "Authorization": "Bearer test-token"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_chat_endpoint_missing_message(mock_user_id):
    """Test that the chat endpoint returns error with missing message"""
    response = client.post(
        f"/api/{mock_user_id}/chat",
        json={},
        headers={
            "Authorization": "Bearer test-token"
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_chat_endpoint_unauthorized(mock_user_id):
    """Test that unauthorized requests are rejected"""
    response = client.post(
        f"/api/{mock_user_id}/chat",
        json={
            "message": "Test message"
        }
        # No Authorization header
    )

    # Expect 401 or 403 depending on your auth middleware
    assert response.status_code in [401, 403]


def test_chat_endpoint_invalid_user_id():
    """Test that invalid user IDs are handled properly"""
    response = client.post(
        "/api/invalid-user-id/chat",
        json={
            "message": "Test message"
        },
        headers={
            "Authorization": "Bearer test-token"
        }
    )

    # Should return 422 for invalid UUID
    assert response.status_code == 422