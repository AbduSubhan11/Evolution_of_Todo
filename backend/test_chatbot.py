#!/usr/bin/env python3
"""
Test script to verify chatbot functionality for task management
"""

import asyncio
import sys
import os

# Add the backend root to the path
backend_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_root)

from src.utils.ai_client import ai_client
from core.tools.task_tools import get_task_tools_for_user
import json
import re

async def test_ai_client_parsing():
    """
    Test the AI client's ability to parse different types of task commands
    """
    print("Testing AI Client Command Parsing...")

    # Create a mock thread ID for testing
    thread_id = "test-thread-123"

    # Test cases for different commands
    test_cases = [
        {
            "message": "Add a task to buy groceries",
            "expected_tool": "add_task",
            "expected_args": {"title": "buy groceries"}
        },
        {
            "message": "Create a task called 'walk the dog'",
            "expected_tool": "add_task",
            "expected_args": {"title": "walk the dog"}
        },
        {
            "message": "Show me my tasks",
            "expected_tool": "list_tasks",
            "expected_args": {}
        },
        {
            "message": "List my completed tasks",
            "expected_tool": "list_tasks",
            "expected_args": {"status_filter": "completed"}
        },
        {
            "message": "Complete the task with title 'buy groceries'",
            "expected_tool": "complete_task",
            "expected_args": {"title": "buy groceries"}
        },
        {
            "message": "Delete the task titled 'walk the dog'",
            "expected_tool": "delete_task",
            "expected_args": {"title": "walk the dog"}
        },
        {
            "message": "Update the task 'buy groceries' to 'buy groceries and cook dinner'",
            "expected_tool": "update_task",
            "expected_args": {"title": "buy groceries and cook dinner"}
        }
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['message']}")

        # Simulate adding message to thread
        ai_client.chat_history = [{"role": "user", "parts": [test_case["message"]]}]

        try:
            response, run_id = await ai_client.run_assistant(thread_id, "test-assistant")

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    function_name = tool_call["function"]["name"]
                    arguments = json.loads(tool_call["function"]["arguments"])

                    print(f"  Detected tool: {function_name}")
                    print(f"  Arguments: {arguments}")

                    # Check if the detected tool matches expected
                    if function_name == test_case["expected_tool"]:
                        print(f"  ✓ Correct tool detected")
                    else:
                        print(f"  ✗ Expected {test_case['expected_tool']}, got {function_name}")
            else:
                print(f"  No tool calls detected")

        except Exception as e:
            print(f"  Error: {e}")

async def test_tool_definitions():
    """
    Test that the tool definitions are properly set up
    """
    print("\nTesting Tool Definitions...")

    # Mock user ID for testing
    user_id = "123e4567-e89b-12d3-a456-426614174000"

    tools = await get_task_tools_for_user(user_id)

    print(f"Retrieved {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool['function']['name']}")
        params = tool['function']['parameters']['properties']
        print(f"    Parameters: {list(params.keys())}")

        # Check that all required fields are optional now for flexible matching
        required_fields = tool['function']['parameters'].get('required', [])
        print(f"    Required: {required_fields}")

async def main():
    print("Testing Chatbot Task Management Functionality\n")
    print("="*50)

    await test_tool_definitions()
    await test_ai_client_parsing()

    print("\n" + "="*50)
    print("Testing completed!")

if __name__ == "__main__":
    asyncio.run(main())