import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from uuid import UUID, uuid4
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.tools.task_tools import (
    get_task_tools_for_user,
    execute_tool_call,
    _add_task,
    _list_tasks,
    _complete_task,
    _delete_task,
    _update_task
)


@pytest.mark.asyncio
async def test_get_task_tools_for_user():
    """Test that get_task_tools_for_user returns the correct tools"""
    user_id = "test-user-id"

    tools = await get_task_tools_for_user(user_id)

    # Verify the structure of the tools
    assert isinstance(tools, list)
    assert len(tools) == 5  # add_task, list_tasks, complete_task, delete_task, update_task

    # Verify each tool has the correct structure
    tool_names = [tool["function"]["name"] for tool in tools]
    expected_names = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    assert set(tool_names) == set(expected_names)


@pytest.mark.asyncio
async def test_execute_tool_call_add_task():
    """Test executing the add_task tool"""
    user_id = str(uuid4())
    tool_name = "add_task"
    arguments = {"title": "Test task", "description": "Test description"}

    with patch('core.tools.task_tools._add_task') as mock_add_task:
        expected_result = {"success": True, "task_id": str(uuid4()), "title": "Test task"}
        mock_add_task.return_value = expected_result

        result = await execute_tool_call(user_id, tool_name, arguments)

        # Verify the result
        assert result == expected_result

        # Verify the function was called with correct parameters
        mock_add_task.assert_called_once()


@pytest.mark.asyncio
async def test_execute_tool_call_list_tasks():
    """Test executing the list_tasks tool"""
    user_id = str(uuid4())
    tool_name = "list_tasks"
    arguments = {"status_filter": "pending"}

    with patch('core.tools.task_tools._list_tasks') as mock_list_tasks:
        expected_result = {"success": True, "tasks": [], "count": 0}
        mock_list_tasks.return_value = expected_result

        result = await execute_tool_call(user_id, tool_name, arguments)

        # Verify the result
        assert result == expected_result

        # Verify the function was called with correct parameters
        mock_list_tasks.assert_called_once()


@pytest.mark.asyncio
async def test_execute_tool_call_unknown_tool():
    """Test executing an unknown tool"""
    user_id = str(uuid4())
    tool_name = "unknown_tool"
    arguments = {}

    result = await execute_tool_call(user_id, tool_name, arguments)

    # Verify the result indicates an error
    assert "error" in result
    assert "Unknown tool" in result["error"]
    assert result["error"] == f"Unknown tool: {tool_name}"


@pytest.mark.asyncio
async def test_add_task_success():
    """Test adding a task successfully"""
    # Create a mock session
    mock_session = AsyncMock()

    # Mock the Task model
    with patch('core.tools.task_tools.Task') as MockTask:
        mock_task_instance = MagicMock()
        mock_task_instance.id = uuid4()
        mock_task_instance.title = "Test task"
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        MockTask.return_value = mock_task_instance

        user_id = str(uuid4())
        args = {"title": "Test task", "description": "Test description"}

        result = await _add_task(mock_session, user_id, args)

        # Verify the result
        assert result["success"] is True
        assert result["title"] == "Test task"
        assert "message" in result

        # Verify the session methods were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_add_task_failure():
    """Test adding a task with failure"""
    mock_session = AsyncMock()
    mock_session.add.side_effect = Exception("Database error")

    user_id = str(uuid4())
    args = {"title": "Test task", "description": "Test description"}

    result = await _add_task(mock_session, user_id, args)

    # Verify the result indicates failure
    assert result["success"] is False
    assert "error" in result
    assert "message" in result


@pytest.mark.asyncio
async def test_list_tasks_success():
    """Test listing tasks successfully"""
    mock_session = AsyncMock()

    # Mock tasks
    mock_task1 = MagicMock()
    mock_task1.id = uuid4()
    mock_task1.title = "Task 1"
    mock_task1.description = "Description 1"
    mock_task1.status = "pending"
    mock_task1.completed_at = None
    mock_task1.created_at = MagicMock()
    mock_task1.updated_at = MagicMock()
    mock_task1.created_at.isoformat.return_value = "2023-01-01T00:00:00"
    mock_task1.updated_at.isoformat.return_value = "2023-01-01T00:00:00"

    mock_task2 = MagicMock()
    mock_task2.id = uuid4()
    mock_task2.title = "Task 2"
    mock_task2.description = "Description 2"
    mock_task2.status = "completed"
    mock_task2.completed_at = MagicMock()
    mock_task2.created_at = MagicMock()
    mock_task2.updated_at = MagicMock()
    mock_task2.completed_at.isoformat.return_value = "2023-01-01T00:00:00"
    mock_task2.created_at.isoformat.return_value = "2023-01-01T00:00:00"
    mock_task2.updated_at.isoformat.return_value = "2023-01-01T00:00:00"

    mock_session.exec.return_value.all.return_value = [mock_task1, mock_task2]

    user_id = str(uuid4())
    args = {}

    result = await _list_tasks(mock_session, user_id, args)

    # Verify the result
    assert result["success"] is True
    assert result["count"] == 2
    assert len(result["tasks"]) == 2


@pytest.mark.asyncio
async def test_complete_task_success():
    """Test completing a task successfully"""
    mock_session = AsyncMock()

    # Mock task
    mock_task = MagicMock()
    mock_task.id = uuid4()
    mock_task.title = "Test task"
    mock_task.status = "pending"
    mock_task.user_id = uuid4()
    mock_session.get.return_value = mock_task

    user_id = str(mock_task.user_id)
    args = {"task_id": str(mock_task.id)}

    result = await _complete_task(mock_session, user_id, args)

    # Verify the result
    assert result["success"] is True
    assert result["title"] == "Test task"
    assert "marked as completed" in result["message"]

    # Verify the session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_success():
    """Test deleting a task successfully"""
    mock_session = AsyncMock()

    # Mock task
    mock_task = MagicMock()
    mock_task.id = uuid4()
    mock_task.title = "Test task"
    mock_task.user_id = uuid4()
    mock_session.get.return_value = mock_task

    user_id = str(mock_task.user_id)
    args = {"task_id": str(mock_task.id)}

    result = await _delete_task(mock_session, user_id, args)

    # Verify the result
    assert result["success"] is True
    assert "deleted successfully" in result["message"]

    # Verify the session methods were called
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_task_success():
    """Test updating a task successfully"""
    mock_session = AsyncMock()

    # Mock task
    mock_task = MagicMock()
    mock_task.id = uuid4()
    mock_task.title = "Old title"
    mock_task.description = "Old description"
    mock_task.user_id = uuid4()
    mock_session.get.return_value = mock_task

    user_id = str(mock_task.user_id)
    args = {"task_id": str(mock_task.id), "title": "New title", "description": "New description"}

    result = await _update_task(mock_session, user_id, args)

    # Verify the result
    assert result["success"] is True
    assert result["title"] == "New title"
    assert "updated successfully" in result["message"]

    # Verify the task attributes were updated
    assert mock_task.title == "New title"
    assert mock_task.description == "New description"

    # Verify the session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()