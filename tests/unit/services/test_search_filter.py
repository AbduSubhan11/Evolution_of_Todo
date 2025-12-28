'''
Unit tests for search and filter functionality in TodoService
'''

import pytest
from src.services.todo_service import TodoService


class TestTodoServiceSearch:
    '''
    Test cases for searching todos in TodoService
    '''

    def test_search_todos_by_keyword(self):
        '''
        Test searching todos by keyword
        '''
        service = TodoService()

        # Add some todos
        service.add_todo("Buy groceries")
        service.add_todo("Walk the dog")
        service.add_todo("Buy milk")

        # Search for todos containing "buy"
        results = service.search_todos("buy")

        assert len(results) == 2
        descriptions = [todo['description'] for todo in results]
        assert "Buy groceries" in descriptions
        assert "Buy milk" in descriptions

    def test_search_todos_case_insensitive(self):
        '''
        Test that searching is case insensitive
        '''
        service = TodoService()

        service.add_todo("Buy groceries")

        results = service.search_todos("BUY")

        assert len(results) == 1
        assert results[0]['description'] == "Buy groceries"

    def test_search_todos_no_matches(self):
        '''
        Test searching for todos with no matches
        '''
        service = TodoService()

        service.add_todo("Buy groceries")

        results = service.search_todos("xyz")

        assert len(results) == 0

    def test_search_todos_empty_keyword(self):
        '''
        Test searching with an empty keyword
        '''
        service = TodoService()

        service.add_todo("Test todo")

        results = service.search_todos("")

        assert len(results) == 0

    def test_search_todos_partial_match(self):
        '''
        Test searching for partial matches in todo descriptions
        '''
        service = TodoService()

        service.add_todo("Complete project documentation")
        service.add_todo("Review code changes")
        service.add_todo("Update project files")

        results = service.search_todos("project")

        assert len(results) == 2
        descriptions = [todo['description'] for todo in results]
        assert "Complete project documentation" in descriptions
        assert "Update project files" in descriptions


class TestTodoServiceFilter:
    '''
    Test cases for filtering todos in TodoService
    '''

    def test_filter_todos_by_status_completed(self):
        '''
        Test filtering todos by completion status (completed)
        '''
        service = TodoService()

        service.add_todo("Completed task", completed=True)
        service.add_todo("Incomplete task", completed=False)

        results = service.filter_todos(status="completed")

        assert len(results) == 1
        assert results[0]['completed'] == True

    def test_filter_todos_by_status_incomplete(self):
        '''
        Test filtering todos by completion status (incomplete)
        '''
        service = TodoService()

        service.add_todo("Completed task", completed=True)
        service.add_todo("Incomplete task", completed=False)

        results = service.filter_todos(status="incomplete")

        assert len(results) == 1
        assert results[0]['completed'] == False

    def test_filter_todos_by_priority_high(self):
        '''
        Test filtering todos by priority (high)
        '''
        service = TodoService()

        service.add_todo("High priority", priority="high")
        service.add_todo("Low priority", priority="low")
        service.add_todo("Medium priority", priority="medium")

        results = service.filter_todos(priority="high")

        assert len(results) == 1
        assert results[0]['priority'] == "high"

    def test_filter_todos_by_priority_medium(self):
        '''
        Test filtering todos by priority (medium)
        '''
        service = TodoService()

        service.add_todo("High priority", priority="high")
        service.add_todo("Low priority", priority="low")
        service.add_todo("Medium priority", priority="medium")

        results = service.filter_todos(priority="medium")

        assert len(results) == 1
        assert results[0]['priority'] == "medium"

    def test_filter_todos_by_due_date(self):
        '''
        Test filtering todos by due date
        '''
        service = TodoService()

        service.add_todo("Task with due date", due_date="2023-12-31")
        service.add_todo("Task without due date")

        results = service.filter_todos(due_date="2023-12-31")

        assert len(results) == 1
        assert results[0]['due_date'] is not None

    def test_filter_todos_invalid_date_format(self):
        '''
        Test filtering todos with invalid date format
        '''
        service = TodoService()

        service.add_todo("Test todo")

        with pytest.raises(ValueError) as exc_info:
            service.filter_todos(due_date="invalid-date")

        assert "Invalid date format" in str(exc_info.value)

    def test_filter_todos_multiple_criteria(self):
        '''
        Test filtering todos by multiple criteria
        '''
        service = TodoService()

        service.add_todo("Completed high priority", completed=True, priority="high")
        service.add_todo("Completed low priority", completed=True, priority="low")
        service.add_todo("Incomplete high priority", completed=False, priority="high")

        results = service.filter_todos(status="completed", priority="high")

        assert len(results) == 1
        assert results[0]['completed'] == True
        assert results[0]['priority'] == "high"

    def test_filter_todos_no_filters(self):
        '''
        Test filtering with no criteria (should return all todos)
        '''
        service = TodoService()

        service.add_todo("Todo 1")
        service.add_todo("Todo 2")

        results = service.filter_todos()

        assert len(results) == 2

    def test_filter_todos_nonexistent_status(self):
        '''
        Test filtering with invalid status value
        '''
        service = TodoService()

        service.add_todo("Test todo")

        # This should not raise an error, but return an empty list since no todos match the invalid status
        results = service.filter_todos(status="invalid_status")

        assert len(results) == 0