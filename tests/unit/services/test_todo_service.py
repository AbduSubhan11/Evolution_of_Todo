'''
Unit tests for TodoService in the Console Todo Application
Tests for updating and deleting todos functionality
'''

import pytest
from src.services.todo_service import TodoService


class TestTodoServiceUpdate:
    '''
    Test cases for updating todo details in TodoService
    '''

    def test_update_todo_description(self):
        '''
        Test updating a todo's description
        '''
        service = TodoService()

        # Add a todo first
        original_todo = service.add_todo("Original description")

        # Update the description
        updated_todo = service.update_todo(original_todo['id'], description="Updated description")

        assert updated_todo is not None
        assert updated_todo['description'] == "Updated description"
        assert updated_todo['id'] == original_todo['id']

    def test_update_todo_priority(self):
        '''
        Test updating a todo's priority
        '''
        service = TodoService()

        # Add a todo first
        original_todo = service.add_todo("Test todo", priority="low")

        # Update the priority
        updated_todo = service.update_todo(original_todo['id'], priority="high")

        assert updated_todo is not None
        assert updated_todo['priority'] == "high"

    def test_update_todo_due_date(self):
        '''
        Test updating a todo's due date
        '''
        service = TodoService()

        # Add a todo first
        original_todo = service.add_todo("Test todo")

        # Update the due date
        updated_todo = service.update_todo(original_todo['id'], due_date="2023-12-31")

        assert updated_todo is not None
        assert updated_todo['due_date'] is not None

    def test_update_todo_completed_status(self):
        '''
        Test updating a todo's completion status
        '''
        service = TodoService()

        # Add a todo first
        original_todo = service.add_todo("Test todo", completed=False)

        # Update the completion status
        updated_todo = service.update_todo(original_todo['id'], completed=True)

        assert updated_todo is not None
        assert updated_todo['completed'] == True

    def test_update_todo_multiple_fields(self):
        '''
        Test updating multiple fields of a todo at once
        '''
        service = TodoService()

        # Add a todo first
        original_todo = service.add_todo("Original", priority="low")

        # Update multiple fields
        updated_todo = service.update_todo(
            original_todo['id'],
            description="Updated description",
            priority="high",
            completed=True
        )

        assert updated_todo is not None
        assert updated_todo['description'] == "Updated description"
        assert updated_todo['priority'] == "high"
        assert updated_todo['completed'] == True

    def test_update_todo_not_found(self):
        '''
        Test updating a todo that doesn't exist
        '''
        service = TodoService()

        result = service.update_todo(999, description="Updated description")

        assert result is None

    def test_update_todo_invalid_date_format(self):
        '''
        Test updating a todo with invalid date format
        '''
        service = TodoService()

        # Add a todo first
        original_todo = service.add_todo("Test todo")

        with pytest.raises(ValueError) as exc_info:
            service.update_todo(original_todo['id'], due_date="invalid-date")

        assert "Invalid date format" in str(exc_info.value)


class TestTodoServiceDelete:
    '''
    Test cases for deleting todos in TodoService
    '''

    def test_delete_todo_success(self):
        '''
        Test successfully deleting a todo
        '''
        service = TodoService()

        # Add a todo first
        todo = service.add_todo("Test todo to delete")

        # Delete the todo
        result = service.delete_todo(todo['id'])

        assert result == True

        # Verify it's gone
        all_todos = service.get_all_todos()
        assert len(all_todos) == 0

    def test_delete_todo_not_found(self):
        '''
        Test deleting a todo that doesn't exist
        '''
        service = TodoService()

        with pytest.raises(ValueError) as exc_info:
            service.delete_todo(999)

        assert "does not exist" in str(exc_info.value)

    def test_delete_todo_then_verify_gone(self):
        '''
        Test that deleting a todo actually removes it from the list
        '''
        service = TodoService()

        # Add multiple todos
        todo1 = service.add_todo("Todo 1")
        todo2 = service.add_todo("Todo 2")
        todo3 = service.add_todo("Todo 3")

        # Delete the second one
        service.delete_todo(todo2['id'])

        # Verify it's gone but others remain
        remaining_todos = service.get_all_todos()
        assert len(remaining_todos) == 2
        ids = [todo['id'] for todo in remaining_todos]
        assert todo1['id'] in ids
        assert todo3['id'] in ids
        assert todo2['id'] not in ids

    def test_delete_all_todos(self):
        '''
        Test deleting all todos
        '''
        service = TodoService()

        # Add multiple todos
        service.add_todo("Todo 1")
        service.add_todo("Todo 2")

        # Delete all of them
        all_todos = service.get_all_todos()
        for todo in all_todos:
            service.delete_todo(todo['id'])

        # Verify the list is empty
        final_todos = service.get_all_todos()
        assert len(final_todos) == 0


class TestTodoServiceToggleCompletion:
    '''
    Test cases for toggling todo completion status in TodoService
    '''

    def test_toggle_completion_from_false_to_true(self):
        '''
        Test toggling completion status from false to true
        '''
        service = TodoService()

        # Add a todo with completed=False
        todo = service.add_todo("Test todo", completed=False)

        # Toggle completion
        updated_todo = service.toggle_completion(todo['id'])

        assert updated_todo is not None
        assert updated_todo['completed'] == True

    def test_toggle_completion_from_true_to_false(self):
        '''
        Test toggling completion status from true to false
        '''
        service = TodoService()

        # Add a todo with completed=True
        todo = service.add_todo("Test todo", completed=True)

        # Toggle completion
        updated_todo = service.toggle_completion(todo['id'])

        assert updated_todo is not None
        assert updated_todo['completed'] == False

    def test_toggle_completion_not_found(self):
        '''
        Test toggling completion for a todo that doesn't exist
        '''
        service = TodoService()

        result = service.toggle_completion(999)

        assert result is None