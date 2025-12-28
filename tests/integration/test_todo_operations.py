'''
Integration tests for adding and viewing todos in the Console Todo Application
'''

from src.models.todo import TodoList


class TestTodoOperationsIntegration:
    '''
    Integration tests for adding and viewing todos functionality
    '''

    def test_add_and_view_single_todo(self):
        '''
        Test adding a single todo and then viewing it
        '''
        todo_list = TodoList()

        # Add a todo
        added_todo = todo_list.add_todo("Test todo")

        # View all todos
        todos = todo_list.get_all_todos()

        assert len(todos) == 1
        assert todos[0].id == added_todo.id
        assert todos[0].description == "Test todo"
        assert todos[0].completed == False

    def test_add_and_view_multiple_todos(self):
        '''
        Test adding multiple todos and then viewing them all
        '''
        todo_list = TodoList()

        # Add multiple todos
        todo1 = todo_list.add_todo("First todo")
        todo2 = todo_list.add_todo("Second todo")
        todo3 = todo_list.add_todo("Third todo")

        # View all todos
        todos = todo_list.get_all_todos()

        assert len(todos) == 3
        assert todos[0].id == todo1.id
        assert todos[1].id == todo2.id
        assert todos[2].id == todo3.id
        assert todos[0].description == "First todo"
        assert todos[1].description == "Second todo"
        assert todos[2].description == "Third todo"

    def test_add_todo_then_view_preserves_attributes(self):
        '''
        Test that adding a todo with specific attributes preserves them when viewed
        '''
        todo_list = TodoList()

        # Add a todo with specific attributes
        added_todo = todo_list.add_todo(
            description="Important task",
            priority="high",
            completed=False
        )

        # View all todos
        todos = todo_list.get_all_todos()

        assert len(todos) == 1
        assert todos[0].description == "Important task"
        assert todos[0].priority == "high"
        assert todos[0].completed == False

    def test_add_todos_with_different_priorities(self):
        '''
        Test adding todos with different priorities and viewing them
        '''
        todo_list = TodoList()

        # Add todos with different priorities
        todo_list.add_todo("Low priority task", priority="low")
        todo_list.add_todo("Medium priority task", priority="medium")
        todo_list.add_todo("High priority task", priority="high")

        # View all todos
        todos = todo_list.get_all_todos()

        assert len(todos) == 3
        priorities = [todo.priority for todo in todos]
        assert "low" in priorities
        assert "medium" in priorities
        assert "high" in priorities

    def test_add_empty_list_then_add_todo(self):
        '''
        Test that viewing an empty list returns empty, then adding a todo makes it visible
        '''
        todo_list = TodoList()

        # Initially, list should be empty
        initial_todos = todo_list.get_all_todos()
        assert len(initial_todos) == 0

        # Add a todo
        todo_list.add_todo("New todo")

        # Now list should have one todo
        updated_todos = todo_list.get_all_todos()
        assert len(updated_todos) == 1
        assert updated_todos[0].description == "New todo"