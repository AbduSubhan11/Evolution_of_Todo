'''
Unit tests for Todo creation in the Console Todo Application
'''

import pytest
from datetime import datetime
from src.models.todo import Todo


class TestTodoCreation:
    '''
    Test cases for Todo creation functionality
    '''

    def test_create_todo_with_valid_data(self):
        '''
        Test creating a todo with valid data
        '''
        todo = Todo(
            id=1,
            description="Test todo",
            completed=False,
            priority="medium",
            created_date=datetime.now(),
            due_date=None
        )

        assert todo.id == 1
        assert todo.description == "Test todo"
        assert todo.completed == False
        assert todo.priority == "medium"
        assert todo.due_date is None

    def test_create_todo_defaults(self):
        '''
        Test creating a todo with default values
        '''
        todo = Todo(id=1, description="Test todo")

        assert todo.id == 1
        assert todo.description == "Test todo"
        assert todo.completed == False
        assert todo.priority == "medium"  # Default priority
        assert todo.created_date is not None  # Should be set to current time

    def test_create_todo_with_priority(self):
        '''
        Test creating a todo with different priority levels
        '''
        todo = Todo(id=1, description="Test todo", priority="high")

        assert todo.priority == "high"

    def test_create_todo_with_due_date(self):
        '''
        Test creating a todo with a due date
        '''
        due_date = datetime(2023, 12, 31)
        todo = Todo(id=1, description="Test todo", due_date=due_date)

        assert todo.due_date == due_date

    def test_create_todo_empty_description_raises_error(self):
        '''
        Test that creating a todo with empty description raises an error
        '''
        with pytest.raises(ValueError) as exc_info:
            Todo(id=1, description="")

        assert "Description must not be empty" in str(exc_info.value)

    def test_create_todo_whitespace_description_raises_error(self):
        '''
        Test that creating a todo with whitespace-only description raises an error
        '''
        with pytest.raises(ValueError) as exc_info:
            Todo(id=1, description="   ")

        assert "Description must not be empty" in str(exc_info.value)

    def test_create_todo_invalid_priority_raises_error(self):
        '''
        Test that creating a todo with invalid priority raises an error
        '''
        with pytest.raises(ValueError) as exc_info:
            Todo(id=1, description="Test todo", priority="invalid")

        assert "Priority must be one of 'low', 'medium', 'high'" in str(exc_info.value)

    def test_toggle_completion(self):
        '''
        Test toggling the completion status of a todo
        '''
        todo = Todo(id=1, description="Test todo", completed=False)

        # Toggle from False to True
        todo.toggle_completion()
        assert todo.completed == True

        # Toggle from True to False
        todo.toggle_completion()
        assert todo.completed == False

    def test_to_dict(self):
        '''
        Test converting a todo to dictionary representation
        '''
        due_date = datetime(2023, 12, 31)
        todo = Todo(
            id=1,
            description="Test todo",
            completed=True,
            priority="high",
            due_date=due_date
        )

        todo_dict = todo.to_dict()

        assert todo_dict['id'] == 1
        assert todo_dict['description'] == "Test todo"
        assert todo_dict['completed'] == True
        assert todo_dict['priority'] == "high"
        assert todo_dict['due_date'] is not None

    def test_from_dict(self):
        '''
        Test creating a Todo object from dictionary representation
        '''
        todo_data = {
            'id': 1,
            'description': 'Test todo',
            'completed': True,
            'priority': 'high',
            'created_date': datetime(2023, 1, 1).isoformat(),
            'due_date': datetime(2023, 12, 31).isoformat()
        }

        todo = Todo.from_dict(todo_data)

        assert todo.id == 1
        assert todo.description == "Test todo"
        assert todo.completed == True
        assert todo.priority == "high"