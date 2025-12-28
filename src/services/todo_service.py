'''
TodoService for the Console Todo Application
Implements the business logic for todo operations as specified in the API contract
'''

import sys
import os
# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models.todo import Todo, TodoList


class TodoService:
    '''
    Service class that implements the business logic for todo operations
    following the API contract defined in the specification
    '''

    def __init__(self):
        '''
        Initialize the TodoService with an in-memory TodoList
        '''
        self.todo_list = TodoList()

    def add_todo(self, description: str, priority: str = 'medium',
                 due_date: Optional[str] = None, completed: bool = False) -> Dict[str, Any]:
        '''
        Add a new todo to the list

        Args:
            description: The task description (required)
            priority: Priority level ('low', 'medium', 'high') - defaults to 'medium'
            due_date: Optional due date in YYYY-MM-DD format
            completed: Completion status - defaults to False

        Returns:
            Todo object with all attributes including generated ID

        Raises:
            ValueError: If description is empty
        '''
        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Invalid date format: {due_date}. Expected YYYY-MM-DD")

        # Validate description
        if not description or not description.strip():
            raise ValueError("Description must not be empty")

        # Add the todo to the list
        todo = self.todo_list.add_todo(
            description=description,
            priority=priority,
            due_date=due_date_obj
        )

        # Set completed status after creation
        todo.completed = completed

        return todo.to_dict()

    def get_all_todos(self) -> List[Dict[str, Any]]:
        '''
        Retrieve all todos in the list

        Returns:
            List of all todo objects
        '''
        todos = self.todo_list.get_all_todos()
        return [todo.to_dict() for todo in todos]

    def update_todo(self, todo_id: int, description: str = None, priority: str = None,
                    due_date: str = None, completed: bool = None) -> Optional[Dict[str, Any]]:
        '''
        Update an existing todo's attributes

        Args:
            todo_id: The ID of the todo to update
            description: New description (optional)
            priority: New priority (optional)
            due_date: New due date (optional) - in YYYY-MM-DD format
            completed: New completion status (optional)

        Returns:
            Updated todo object if successful, None if todo not found

        Raises:
            ValueError: If todo_id doesn't exist or if date format is invalid
        '''
        # Parse due_date if provided
        due_date_obj = None
        if due_date is not None:  # Explicitly check for None to allow empty string
            if due_date:  # Only parse if not empty string
                try:
                    due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError(f"Invalid date format: {due_date}. Expected YYYY-MM-DD")

        # Update the todo
        updated_todo = self.todo_list.update_todo(
            todo_id=todo_id,
            description=description,
            priority=priority,
            due_date=due_date_obj,
            completed=completed
        )

        if updated_todo:
            return updated_todo.to_dict()
        else:
            return None

    def delete_todo(self, todo_id: int) -> bool:
        '''
        Remove a todo from the list

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if deletion was successful, False if todo not found

        Raises:
            ValueError: If todo_id doesn't exist
        '''
        success = self.todo_list.delete_todo(todo_id)
        if not success:
            raise ValueError(f"Todo with ID {todo_id} does not exist")
        return success

    def toggle_completion(self, todo_id: int) -> Optional[Dict[str, Any]]:
        '''
        Toggle the completion status of a todo

        Args:
            todo_id: The ID of the todo to update

        Returns:
            Updated todo object if successful, None if todo not found

        Raises:
            ValueError: If todo_id doesn't exist
        '''
        todo = self.todo_list.toggle_completion(todo_id)
        if todo:
            return todo.to_dict()
        else:
            return None

    def search_todos(self, keyword: str) -> List[Dict[str, Any]]:
        '''
        Find todos containing the keyword in their description

        Args:
            keyword: The text to search for

        Returns:
            List of matching todo objects
        '''
        todos = self.todo_list.search_todos(keyword)
        return [todo.to_dict() for todo in todos]

    def filter_todos(self, status: str = None, priority: str = None,
                     due_date: str = None) -> List[Dict[str, Any]]:
        '''
        Filter todos by specified criteria

        Args:
            status: Filter by completion status ('completed', 'incomplete')
            priority: Filter by priority ('low', 'medium', 'high')
            due_date: Filter by due date (specific date in YYYY-MM-DD format)

        Returns:
            List of matching todo objects
        '''
        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Invalid date format: {due_date}. Expected YYYY-MM-DD")

        todos = self.todo_list.filter_todos(
            status=status,
            priority=priority,
            due_date=due_date_obj
        )
        return [todo.to_dict() for todo in todos]