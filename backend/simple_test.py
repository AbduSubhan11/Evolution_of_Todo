#!/usr/bin/env python3
"""
Simple test script to verify chatbot functionality for task management
"""

import asyncio
import sys
import os
import json
import re

# Add the backend root to the path
backend_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_root)

from src.utils.ai_client import AIClient

async def test_ai_client_parsing():
    """
    Test the AI client's ability to parse different types of task commands
    """
    print("Testing AI Client Command Parsing...")

    # Create a new AI client instance for testing
    ai_client = AIClient()

    # Test cases for different commands
    test_cases = [
        {
            "message": "Add a task to buy groceries",
            "expected_tool": "add_task",
        },
        {
            "message": "Create a task called 'walk the dog'",
            "expected_tool": "add_task",
        },
        {
            "message": "Show me my tasks",
            "expected_tool": "list_tasks",
        },
        {
            "message": "List my completed tasks",
            "expected_tool": "list_tasks",
        },
        {
            "message": "Complete the task with title 'buy groceries'",
            "expected_tool": "complete_task",
        },
        {
            "message": "Delete the task titled 'walk the dog'",
            "expected_tool": "delete_task",
        },
        {
            "message": "Update the task 'buy groceries' to 'buy groceries and cook dinner'",
            "expected_tool": "update_task",
        }
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['message']}")

        # Simulate adding message to thread
        ai_client.chat_history = [{"role": "user", "parts": [test_case["message"]]}]

        try:
            response, run_id = await ai_client.run_assistant("test-thread-123", "test-assistant")

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    function_name = tool_call["function"]["name"]
                    arguments = json.loads(tool_call["function"]["arguments"])

                    print(f"  Detected tool: {function_name}")
                    print(f"  Arguments: {arguments}")

                    # Check if the detected tool matches expected (at least partially)
                    if function_name == test_case["expected_tool"]:
                        print(f"  ✓ Correct tool detected")
                    else:
                        print(f"  ~ Detected: {function_name} (Expected: {test_case['expected_tool']})")
            else:
                print(f"  No tool calls detected")

        except Exception as e:
            print(f"  Error: {e}")

async def main():
    print("Testing Chatbot Task Management Functionality\n")
    print("="*50)

    await test_ai_client_parsing()

    print("\n" + "="*50)
    print("Testing completed!")

if __name__ == "__main__":
    asyncio.run(main())