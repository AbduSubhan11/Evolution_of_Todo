'''
Todo model for the Console Todo Application
Implements the Todo entity and TodoList collection as specified in the data model
'''

from datetime import datetime
from typing import List, Optional, Dict, Any
import json


class Todo:
    '''
    Represents a single todo item with attributes as specified in the data model
    '''

    def __init__(self, id: int, description: str, completed: bool = False,
                 priority: str = 'medium', created_date: datetime = None,
                 due_date: Optional[datetime] = None):
        '''
        Initialize a Todo object

        Args:
            id: Unique identifier for the todo
            description: Task description (required)
            completed: Completion status (default: False)
            priority: Priority level ('low', 'medium', 'high') (default: 'medium')
            created_date: Date when todo was created (default: current datetime)
            due_date: Optional due date
        '''
        self.id = id
        self.description = description
        self.completed = completed
        self.priority = priority
        self.created_date = created_date or datetime.now()
        self.due_date = due_date

        # Validate inputs
        self._validate()

    def _validate(self):
        '''
        Validate the todo attributes according to the data model
        '''
        if not self.description or not self.description.strip():
            raise ValueError("Description must not be empty")

        if self.priority not in ['low', 'medium', 'high']:
            raise ValueError(f"Priority must be one of 'low', 'medium', 'high', got '{self.priority}'")

    def toggle_completion(self):
        '''
        Toggle the completion status of the todo
        '''
        self.completed = not self.completed

    def to_dict(self) -> Dict[str, Any]:
        '''
        Convert the todo to a dictionary representation

        Returns:
            Dictionary representation of the todo
        '''
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Todo':
        '''
        Create a Todo object from a dictionary representation

        Args:
            data: Dictionary representation of a todo

        Returns:
            Todo object
        '''
        # Convert ISO format strings back to datetime objects if they exist
        created_date = datetime.fromisoformat(data['created_date']) if data['created_date'] else None
        due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None

        return cls(
            id=data['id'],
            description=data['description'],
            completed=data['completed'],
            priority=data['priority'],
            created_date=created_date,
            due_date=due_date
        )


class TodoList:
    '''
    Collection of Todo items stored in memory as an array
    '''

    def __init__(self):
        '''
        Initialize an empty TodoList with a counter for generating unique IDs
        '''
        self.todos: List[Todo] = []
        self.next_id = 1

    def add_todo(self, description: str, priority: str = 'medium',
                 due_date: Optional[datetime] = None, completed: bool = False) -> Todo:
        '''
        Add a new todo to the list

        Args:
            description: Task description
            priority: Priority level ('low', 'medium', 'high') (default: 'medium')
            due_date: Optional due date
            completed: Completion status (default: False)

        Returns:
            The newly created Todo object
        '''
        todo = Todo(
            id=self.next_id,
            description=description,
            completed=completed,
            priority=priority,
            due_date=due_date
        )
        self.todos.append(todo)
        self.next_id += 1
        return todo

    def get_all_todos(self) -> List[Todo]:
        '''
        Get all todos in the list

        Returns:
            List of all Todo objects
        '''
        return self.todos.copy()  # Return a copy to prevent external modification

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        '''
        Get a specific todo by its ID

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            Todo object if found, None otherwise
        '''
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(self, todo_id: int, description: str = None,
                    priority: str = None, due_date: datetime = None,
                    completed: bool = None) -> Optional[Todo]:
        '''
        Update an existing todo's attributes

        Args:
            todo_id: The ID of the todo to update
            description: New description (optional)
            priority: New priority (optional)
            due_date: New due date (optional)
            completed: New completion status (optional)

        Returns:
            Updated Todo object if successful, None if todo not found
        '''
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return None

        if description is not None:
            todo.description = description
        if priority is not None:
            todo.priority = priority
        if due_date is not None:
            todo.due_date = due_date
        if completed is not None:
            todo.completed = completed

        # Re-validate after updates
        todo._validate()
        return todo

    def delete_todo(self, todo_id: int) -> bool:
        '''
        Remove a todo from the list by ID

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if deletion was successful, False if todo not found
        '''
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                return True
        return False

    def toggle_completion(self, todo_id: int) -> Optional[Todo]:
        '''
        Toggle the completion status of a todo

        Args:
            todo_id: The ID of the todo to update

        Returns:
            Updated Todo object if successful, None if todo not found
        '''
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.toggle_completion()
            return todo
        return None

    def search_todos(self, keyword: str) -> List[Todo]:
        '''
        Find todos containing the keyword in their description

        Args:
            keyword: The text to search for

        Returns:
            List of matching Todo objects
        '''
        if not keyword or not keyword.strip():
            # If keyword is empty or only whitespace, return no results
            return []

        keyword_lower = keyword.lower().strip()
        return [todo for todo in self.todos
                if keyword_lower in todo.description.lower()]

    def filter_todos(self, status: str = None, priority: str = None,
                     due_date: datetime = None) -> List[Todo]:
        '''
        Filter todos by specified criteria

        Args:
            status: Filter by completion status ('completed', 'incomplete')
            priority: Filter by priority ('low', 'medium', 'high')
            due_date: Filter by due date (exact date match)

        Returns:
            List of matching Todo objects
        '''
        result = self.todos.copy()

        if status:
            if status == 'completed':
                result = [todo for todo in result if todo.completed]
            elif status == 'incomplete':
                result = [todo for todo in result if not todo.completed]
            else:
                # For invalid status values, return an empty list since no todos would match
                result = []

        if priority:
            if priority in ['low', 'medium', 'high']:
                result = [todo for todo in result if todo.priority == priority]
            else:
                # For invalid priority values, return an empty list since no todos would match
                result = []

        if due_date:
            result = [todo for todo in result
                      if todo.due_date and todo.due_date.date() == due_date.date()]

        return result