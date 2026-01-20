import sys
import os
from datetime import datetime

# Add the backend root directory to the Python path
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Go from core/tools to backend root
sys.path.append(backend_root)

from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from uuid import UUID
from src.database import get_session_context
from src.models.task import Task, TaskCreate, TaskUpdate
import json
from contextlib import asynccontextmanager

async def get_task_tools_for_user(user_id: str) -> List[Dict[str, Any]]:
    """
    Returns the OpenAI-compatible tool definitions for task operations for a specific user
    """
    tools = [
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
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task to complete (partial match allowed)"
                        }
                    },
                    "required": []
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
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task to delete (partial match allowed)"
                        }
                    },
                    "required": []
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
                        "existing_title": {
                            "type": "string",
                            "description": "The current title of the task to update (partial match allowed)"
                        },
                        "title": {
                            "type": "string",
                            "description": "The new title for the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "The new description for the task"
                        },
                        "status": {
                            "type": "string",
                            "description": "The new status for the task (pending, completed, archived)",
                            "enum": ["pending", "completed", "archived"]
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "uncomplete_task",
                "description": "Mark a task as pending/uncompleted",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to uncomplete"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task to uncomplete (partial match allowed)"
                        }
                    },
                    "required": []
                }
            }
        }
    ]

    return tools

async def execute_tool_call(user_id: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool call with the given arguments for the specified user
    """
    async with get_session_context() as session:
        if tool_name == "add_task":
            return await _add_task(session, user_id, arguments)
        elif tool_name == "list_tasks":
            return await _list_tasks(session, user_id, arguments)
        elif tool_name == "complete_task":
            return await _complete_task(session, user_id, arguments)
        elif tool_name == "delete_task":
            return await _delete_task(session, user_id, arguments)
        elif tool_name == "update_task":
            return await _update_task(session, user_id, arguments)
        elif tool_name == "uncomplete_task":
            return await _uncomplete_task(session, user_id, arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

async def _uncomplete_task(session: Session, user_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a task as pending/uncompleted
    """
    try:
        task_id = args.get("task_id")
        task_title = args.get("title")

        # Find the task by either ID or title
        db_task = None

        if task_id:
            try:
                db_task = session.get(Task, UUID(task_id))
            except ValueError:
                return {"success": False, "error": "Invalid task ID format", "message": "Invalid task ID format"}
        elif task_title:
            # Find task by title for the user
            statement = select(Task).where(
                Task.user_id == UUID(user_id),
                Task.title.ilike(f"%{task_title}%")  # Case-insensitive partial match
            )
            tasks = session.exec(statement).all()

            if not tasks:
                return {"success": False, "error": "Task not found", "message": f"No task found with title containing '{task_title}'"}
            elif len(tasks) > 1:
                # If multiple tasks match, return a list of possible matches
                task_list = [{"id": str(t.id), "title": t.title} for t in tasks]
                return {
                    "success": False,
                    "error": "Multiple tasks found",
                    "message": f"Multiple tasks found with title '{task_title}'. Please specify by ID.",
                    "possible_matches": task_list
                }
            else:
                db_task = tasks[0]
        else:
            return {"success": False, "error": "task_id or title is required", "message": "Task ID or title is required"}

        if not db_task:
            return {"success": False, "error": "Task not found", "message": "Task not found"}

        # Verify that the task belongs to the user
        if str(db_task.user_id) != user_id:
            return {"success": False, "error": "Unauthorized", "message": "You don't have permission to modify this task"}

        # Update task status to pending
        db_task.status = "pending"
        db_task.completed_at = None  # Clear completion timestamp
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "success": True,
            "task_id": str(db_task.id),
            "title": db_task.title,
            "status": db_task.status,
            "message": f"Task '{db_task.title}' marked as pending"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to uncomplete task"
        }

async def _add_task(session: Session, user_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new task for the user
    """
    try:
        title = args.get("title")
        if not title:
            return {
                "success": False,
                "error": "Title is required",
                "message": "Task title is required"
            }

        # Create task data with user_id
        task_data = {
            "title": title,
            "description": args.get("description", ""),
            "user_id": UUID(user_id)
        }

        db_task = Task(**task_data)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "success": True,
            "task_id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "message": f"Task '{db_task.title}' added successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add task"
        }

async def _list_tasks(session: Session, user_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    List tasks for the user with optional filtering
    """
    try:
        # Build query to get tasks for the user
        query = select(Task).where(Task.user_id == UUID(user_id))

        # Apply status filter if provided
        status_filter = args.get("status_filter")
        if status_filter:
            query = query.where(Task.status == status_filter)

        # Execute query
        tasks = session.exec(query).all()

        task_list = []
        for task in tasks:
            task_list.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            })

        # Format the message based on filter
        if status_filter:
            message = f"Found {len(task_list)} {status_filter} tasks"
        else:
            message = f"Found {len(task_list)} tasks"

        return {
            "success": True,
            "tasks": task_list,
            "count": len(task_list),
            "status_filter": status_filter,
            "message": message
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list tasks"
        }

async def _complete_task(session: Session, user_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a task as completed
    """
    try:
        task_id = args.get("task_id")
        task_title = args.get("title")

        # Find the task by either ID or title
        db_task = None

        if task_id:
            try:
                db_task = session.get(Task, UUID(task_id))
            except ValueError:
                return {"success": False, "error": "Invalid task ID format", "message": "Invalid task ID format"}
        elif task_title:
            # Find task by title for the user
            statement = select(Task).where(
                Task.user_id == UUID(user_id),
                Task.title.ilike(f"%{task_title}%")  # Case-insensitive partial match
            )
            tasks = session.exec(statement).all()

            if not tasks:
                return {"success": False, "error": "Task not found", "message": f"No task found with title containing '{task_title}'"}
            elif len(tasks) > 1:
                # If multiple tasks match, return a list of possible matches
                task_list = [{"id": str(t.id), "title": t.title} for t in tasks]
                return {
                    "success": False,
                    "error": "Multiple tasks found",
                    "message": f"Multiple tasks found with title '{task_title}'. Please specify by ID.",
                    "possible_matches": task_list
                }
            else:
                db_task = tasks[0]
        else:
            return {"success": False, "error": "task_id or title is required", "message": "Task ID or title is required"}

        if not db_task:
            return {"success": False, "error": "Task not found", "message": "Task not found"}

        # Verify that the task belongs to the user
        if str(db_task.user_id) != user_id:
            return {"success": False, "error": "Unauthorized", "message": "You don't have permission to modify this task"}

        # Update task status
        db_task.status = "completed"
        db_task.completed_at = datetime.utcnow()  # Set completion timestamp
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "success": True,
            "task_id": str(db_task.id),
            "title": db_task.title,
            "status": db_task.status,
            "message": f"Task '{db_task.title}' marked as completed"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to complete task"
        }

async def _delete_task(session: Session, user_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a task for the user
    """
    try:
        task_id = args.get("task_id")
        task_title = args.get("title")

        # Find the task by either ID or title
        db_task = None

        if task_id:
            try:
                db_task = session.get(Task, UUID(task_id))
            except ValueError:
                return {"success": False, "error": "Invalid task ID format", "message": "Invalid task ID format"}
        elif task_title:
            # Find task by title for the user
            statement = select(Task).where(
                Task.user_id == UUID(user_id),
                Task.title.ilike(f"%{task_title}%")  # Case-insensitive partial match
            )
            tasks = session.exec(statement).all()

            if not tasks:
                return {"success": False, "error": "Task not found", "message": f"No task found with title containing '{task_title}'"}
            elif len(tasks) > 1:
                # If multiple tasks match, return a list of possible matches
                task_list = [{"id": str(t.id), "title": t.title} for t in tasks]
                return {
                    "success": False,
                    "error": "Multiple tasks found",
                    "message": f"Multiple tasks found with title '{task_title}'. Please specify by ID.",
                    "possible_matches": task_list
                }
            else:
                db_task = tasks[0]
        else:
            return {"success": False, "error": "task_id or title is required", "message": "Task ID or title is required"}

        if not db_task:
            return {"success": False, "error": "Task not found", "message": "Task not found"}

        # Verify that the task belongs to the user
        if str(db_task.user_id) != user_id:
            return {"success": False, "error": "Unauthorized", "message": "You don't have permission to delete this task"}

        # Delete the task
        session.delete(db_task)
        session.commit()

        return {
            "success": True,
            "task_id": str(db_task.id),
            "title": db_task.title,
            "message": f"Task '{db_task.title}' deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to delete task"
        }

async def _update_task(session: Session, user_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a task for the user
    """
    try:
        task_id = args.get("task_id")
        existing_title = args.get("existing_title")  # Separate field for existing title to find
        new_title = args.get("title")  # New title to update to
        description = args.get("description")  # New description to update to
        status = args.get("status")  # New status to update to

        # Find the task by either ID or title
        db_task = None

        if task_id:
            try:
                db_task = session.get(Task, UUID(task_id))
            except ValueError:
                return {"success": False, "error": "Invalid task ID format", "message": "Invalid task ID format"}
        elif existing_title:
            # Find task by existing title for the user
            statement = select(Task).where(
                Task.user_id == UUID(user_id),
                Task.title.ilike(f"%{existing_title}%")  # Case-insensitive partial match
            )
            tasks = session.exec(statement).all()

            if not tasks:
                return {"success": False, "error": "Task not found", "message": f"No task found with title containing '{existing_title}'"}
            elif len(tasks) > 1:
                # If multiple tasks match, return a list of possible matches
                task_list = [{"id": str(t.id), "title": t.title} for t in tasks]
                return {
                    "success": False,
                    "error": "Multiple tasks found",
                    "message": f"Multiple tasks found with title '{existing_title}'. Please specify by ID.",
                    "possible_matches": task_list
                }
            else:
                db_task = tasks[0]
        elif new_title and description is not None:  # If we only have a new title and description, try to match by content
            # This scenario shouldn't happen often, but just in case
            return {"success": False, "error": "Task to update not specified", "message": "Please specify which task to update."}
        else:
            return {"success": False, "error": "task_id or existing_title is required", "message": "Task ID or existing title is required"}

        if not db_task:
            return {"success": False, "error": "Task not found", "message": "Task not found"}

        # Verify that the task belongs to the user
        if str(db_task.user_id) != user_id:
            return {"success": False, "error": "Unauthorized", "message": "You don't have permission to update this task"}

        # Update task fields if provided
        if new_title is not None and new_title != db_task.title:
            db_task.title = new_title
        if description is not None:
            db_task.description = description
        if status is not None and status != db_task.status:
            db_task.status = status
            # Update completed_at based on status
            if status == "completed":
                if not db_task.completed_at:
                    db_task.completed_at = datetime.utcnow()
            else:
                db_task.completed_at = None  # Reset completion time for non-completed status

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "success": True,
            "task_id": str(db_task.id),
            "title": db_task.title,
            "description": db_task.description,
            "status": db_task.status,
            "message": f"Task '{db_task.title}' updated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update task"
        }