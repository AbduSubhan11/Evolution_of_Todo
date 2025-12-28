'''
Unit tests for TodoList operations in the Console Todo Application
'''

import pytest
from datetime import datetime
from src.models.todo import TodoList


class TestTodoListOperations:
    '''
    Test cases for TodoList operations functionality
    '''

    def test_initial_empty_list(self):
        '''
        Test that a new TodoList is initially empty
        '''
        todo_list = TodoList()

        assert len(todo_list.get_all_todos()) == 0
        assert todo_list.next_id == 1

    def test_add_todo(self):
        '''
        Test adding a todo to the list
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Test todo")

        assert len(todo_list.get_all_todos()) == 1
        assert todo.id == 1
        assert todo.description == "Test todo"
        assert todo_list.next_id == 2

    def test_add_todo_with_priority(self):
        '''
        Test adding a todo with a specific priority
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Test todo", priority="high")

        assert todo.priority == "high"

    def test_add_todo_with_due_date(self):
        '''
        Test adding a todo with a due date
        '''
        todo_list = TodoList()
        due_date = datetime(2023, 12, 31)

        todo = todo_list.add_todo("Test todo", due_date=due_date)

        assert todo.due_date == due_date

    def test_get_all_todos(self):
        '''
        Test getting all todos from the list
        '''
        todo_list = TodoList()

        todo_list.add_todo("Todo 1")
        todo_list.add_todo("Todo 2")

        todos = todo_list.get_all_todos()

        assert len(todos) == 2
        assert todos[0].description == "Todo 1"
        assert todos[1].description == "Todo 2"

    def test_get_todo_by_id_found(self):
        '''
        Test getting a todo by its ID when it exists
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Test todo")

        found_todo = todo_list.get_todo_by_id(todo.id)

        assert found_todo is not None
        assert found_todo.id == todo.id
        assert found_todo.description == "Test todo"

    def test_get_todo_by_id_not_found(self):
        '''
        Test getting a todo by its ID when it doesn't exist
        '''
        todo_list = TodoList()

        todo_list.add_todo("Test todo")

        found_todo = todo_list.get_todo_by_id(999)

        assert found_todo is None

    def test_update_todo_description(self):
        '''
        Test updating a todo's description
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Original todo")
        updated_todo = todo_list.update_todo(todo.id, description="Updated todo")

        assert updated_todo is not None
        assert updated_todo.description == "Updated todo"

    def test_update_todo_priority(self):
        '''
        Test updating a todo's priority
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Test todo", priority="low")
        updated_todo = todo_list.update_todo(todo.id, priority="high")

        assert updated_todo is not None
        assert updated_todo.priority == "high"

    def test_update_todo_due_date(self):
        '''
        Test updating a todo's due date
        '''
        todo_list = TodoList()
        new_due_date = datetime(2023, 12, 31)

        todo = todo_list.add_todo("Test todo")
        updated_todo = todo_list.update_todo(todo.id, due_date=new_due_date)

        assert updated_todo is not None
        assert updated_todo.due_date == new_due_date

    def test_update_todo_completed_status(self):
        '''
        Test updating a todo's completion status
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Test todo", completed=False)
        updated_todo = todo_list.update_todo(todo.id, completed=True)

        assert updated_todo is not None
        assert updated_todo.completed == True

    def test_update_todo_not_found(self):
        '''
        Test updating a todo that doesn't exist
        '''
        todo_list = TodoList()

        result = todo_list.update_todo(999, description="Updated todo")

        assert result is None

    def test_delete_todo_success(self):
        '''
        Test successfully deleting a todo
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Test todo")
        success = todo_list.delete_todo(todo.id)

        assert success == True
        assert len(todo_list.get_all_todos()) == 0

    def test_delete_todo_not_found(self):
        '''
        Test deleting a todo that doesn't exist
        '''
        todo_list = TodoList()

        success = todo_list.delete_todo(999)

        assert success == False

    def test_toggle_completion(self):
        '''
        Test toggling a todo's completion status
        '''
        todo_list = TodoList()

        todo = todo_list.add_todo("Test todo", completed=False)
        toggled_todo = todo_list.toggle_completion(todo.id)

        assert toggled_todo is not None
        assert toggled_todo.completed == True

    def test_toggle_completion_not_found(self):
        '''
        Test toggling completion for a todo that doesn't exist
        '''
        todo_list = TodoList()

        result = todo_list.toggle_completion(999)

        assert result is None

    def test_search_todos(self):
        '''
        Test searching for todos by keyword
        '''
        todo_list = TodoList()

        todo_list.add_todo("Buy groceries")
        todo_list.add_todo("Walk the dog")
        todo_list.add_todo("Buy milk")

        results = todo_list.search_todos("buy")

        assert len(results) == 2
        descriptions = [todo.description for todo in results]
        assert "Buy groceries" in descriptions
        assert "Buy milk" in descriptions

    def test_search_todos_case_insensitive(self):
        '''
        Test that searching is case insensitive
        '''
        todo_list = TodoList()

        todo_list.add_todo("Buy groceries")

        results = todo_list.search_todos("BUY")

        assert len(results) == 1
        assert results[0].description == "Buy groceries"

    def test_search_todos_no_matches(self):
        '''
        Test searching for todos with no matches
        '''
        todo_list = TodoList()

        todo_list.add_todo("Buy groceries")

        results = todo_list.search_todos("xyz")

        assert len(results) == 0

    def test_filter_todos_by_status_completed(self):
        '''
        Test filtering todos by completion status (completed)
        '''
        todo_list = TodoList()

        todo_list.add_todo("Completed todo", completed=True)
        todo_list.add_todo("Incomplete todo", completed=False)

        results = todo_list.filter_todos(status="completed")

        assert len(results) == 1
        assert results[0].completed == True

    def test_filter_todos_by_status_incomplete(self):
        '''
        Test filtering todos by completion status (incomplete)
        '''
        todo_list = TodoList()

        todo_list.add_todo("Completed todo", completed=True)
        todo_list.add_todo("Incomplete todo", completed=False)

        results = todo_list.filter_todos(status="incomplete")

        assert len(results) == 1
        assert results[0].completed == False

    def test_filter_todos_by_priority(self):
        '''
        Test filtering todos by priority
        '''
        todo_list = TodoList()

        todo_list.add_todo("Low priority", priority="low")
        todo_list.add_todo("High priority", priority="high")
        todo_list.add_todo("Medium priority", priority="medium")

        results = todo_list.filter_todos(priority="high")

        assert len(results) == 1
        assert results[0].priority == "high"

    def test_filter_todos_by_due_date(self):
        '''
        Test filtering todos by due date
        '''
        todo_list = TodoList()
        due_date = datetime(2023, 12, 31)

        todo_list.add_todo("Todo with due date", due_date=due_date)
        todo_list.add_todo("Todo without due date")

        results = todo_list.filter_todos(due_date=due_date)

        assert len(results) == 1
        assert results[0].due_date == due_date

    def test_filter_todos_multiple_criteria(self):
        '''
        Test filtering todos by multiple criteria
        '''
        todo_list = TodoList()
        due_date = datetime(2023, 12, 31)

        todo_list.add_todo("Completed high priority", completed=True, priority="high")
        todo_list.add_todo("Completed low priority", completed=True, priority="low")
        todo_list.add_todo("Incomplete high priority", completed=False, priority="high")

        results = todo_list.filter_todos(status="completed", priority="high")

        assert len(results) == 1
        assert results[0].completed == True
        assert results[0].priority == "high"