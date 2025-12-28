# Todo API Contract

## Overview
This contract defines the interface for the Todo application's core functionality. Since this is a console application, these represent the internal service interfaces that will be called by the CLI layer.

## Todo Service Interface

### add_todo(description: str, priority: str = 'medium', due_date: str = None) -> dict
**Description**: Adds a new todo to the list
**Parameters**:
- description: The task description (required)
- priority: Priority level ('low', 'medium', 'high') - defaults to 'medium'
- due_date: Optional due date in YYYY-MM-DD format
**Returns**: Todo object with all attributes including generated ID
**Errors**: ValueError if description is empty

### get_all_todos() -> list
**Description**: Retrieves all todos in the list
**Returns**: List of all todo objects
**Errors**: None

### update_todo(todo_id: int, description: str = None, priority: str = None, due_date: str = None, completed: bool = None) -> dict
**Description**: Updates an existing todo's attributes
**Parameters**:
- todo_id: The ID of the todo to update
- description: New description (optional)
- priority: New priority (optional)
- due_date: New due date (optional)
- completed: New completion status (optional)
**Returns**: Updated todo object
**Errors**: ValueError if todo_id doesn't exist

### delete_todo(todo_id: int) -> bool
**Description**: Removes a todo from the list
**Parameters**:
- todo_id: The ID of the todo to delete
**Returns**: True if deletion was successful, False otherwise
**Errors**: ValueError if todo_id doesn't exist

### toggle_completion(todo_id: int) -> dict
**Description**: Toggles the completion status of a todo
**Parameters**:
- todo_id: The ID of the todo to update
**Returns**: Updated todo object
**Errors**: ValueError if todo_id doesn't exist

### search_todos(keyword: str) -> list
**Description**: Finds todos containing the keyword in their description
**Parameters**:
- keyword: The text to search for
**Returns**: List of matching todo objects
**Errors**: None

### filter_todos(status: str = None, priority: str = None, due_date: str = None) -> list
**Description**: Filters todos by specified criteria
**Parameters**:
- status: Filter by completion status ('completed', 'incomplete')
- priority: Filter by priority ('low', 'medium', 'high')
- due_date: Filter by due date (specific date in YYYY-MM-DD format)
**Returns**: List of matching todo objects
**Errors**: None