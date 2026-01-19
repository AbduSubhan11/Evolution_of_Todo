from typing import Dict, Callable, Any, List
from ...utils.ai_client import ai_client
from ...core.tools.task_tools import execute_tool_call
from uuid import UUID

class ToolRegistry:
    """
    Registry for managing available tools for the AI agent
    """

    def __init__(self):
        self.tools = {}

    async def register_tool(self, name: str, handler: Callable, description: str = ""):
        """
        Register a new tool with the registry
        """
        self.tools[name] = {
            "handler": handler,
            "description": description
        }

    async def execute_tool(self, user_id: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool with the given arguments for the user
        """
        if tool_name not in self.tools:
            return {
                "error": f"Tool '{tool_name}' not found",
                "success": False
            }

        try:
            handler = self.tools[tool_name]["handler"]
            return await handler(user_id, arguments)
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get the OpenAI-compatible tool definitions for all registered tools
        """
        # We'll return the same tools that were defined in task_tools.py
        # In a real implementation, we might have a more sophisticated way to register these

        tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's task list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "The description of the task"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks from the user's task list with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status_filter": {
                                "type": "string",
                                "description": "Filter tasks by status (pending, completed, archived)",
                                "enum": ["pending", "completed", "archived"]
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the user's list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "The new title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "The new description of the task"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

        return tool_definitions

# Global instance
tool_registry = ToolRegistry()

# Register the task tools
async def initialize_tool_registry():
    """
    Initialize the tool registry with all available tools
    """
    await tool_registry.register_tool("add_task", execute_tool_call, "Add a new task to the user's list")
    await tool_registry.register_tool("list_tasks", execute_tool_call, "List tasks with optional filtering")
    await tool_registry.register_tool("complete_task", execute_tool_call, "Mark a task as completed")
    await tool_registry.register_tool("delete_task", execute_tool_call, "Delete a task from the user's list")
    await tool_registry.register_tool("update_task", execute_tool_call, "Update a task's details")