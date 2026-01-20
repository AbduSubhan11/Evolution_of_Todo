import sys
import os

# Add the backend root directory to the Python path
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Go from core/agents to backend root
sys.path.append(backend_root)

from typing import Dict, Any, List
from src.utils.ai_client import ai_client
from core.tools.task_tools import get_task_tools_for_user
from uuid import UUID

async def initialize_chat_agent(user_id: UUID) -> str:
    """
    Initialize a chat agent with the appropriate tools for the given user
    """
    # Get the tools available for this specific user
    tools = await get_task_tools_for_user(str(user_id))

    # Create instructions for the assistant
    instructions = f"""
    You are an AI assistant that ONLY helps users manage their todo tasks through specific function calls. The user's ID is {user_id}. You have access to specific functions to perform operations on the user's tasks.

    You MUST use the available functions for all task management operations. Do not provide generic advice, SQL queries, or instructions on how to perform tasks manually.

    Available functions:
    1. add_task: To add a new task - Use when user wants to create/add a task
    2. list_tasks: To list existing tasks - Use when user wants to see their tasks
    3. complete_task: To mark a task as completed - Use when user wants to mark a task as done
    4. uncomplete_task: To mark a task as pending again - Use when user wants to revert a completed task to pending
    5. delete_task: To delete a task - Use when user wants to remove a task
    6. update_task: To update task details - Use when user wants to change task title, description, or status

    When the user says hello or greets you, respond with: "Hi! I'm your AI assistant. I can help you manage your tasks. What would you like to do? (add, list, update, complete, uncomplete, delete)"

    For any task-related request, identify the appropriate function and call it. Always use function calls instead of providing manual instructions or SQL queries.
    """

    # Create the assistant with the tools
    assistant_id = await ai_client.create_assistant(instructions, tools)
    return assistant_id

async def process_user_message(user_id: UUID, conversation_id: str, message: str) -> Dict[str, Any]:
    """
    Process a user message and return the AI response
    """
    # Initialize the agent if not already done
    assistant_id = await initialize_chat_agent(user_id)

    # Process the message with the AI client
    response = await ai_client.run_assistant(conversation_id, assistant_id)

    return {
        "response": response.content,
        "tool_calls": response.tool_calls,
        "conversation_id": conversation_id
    }