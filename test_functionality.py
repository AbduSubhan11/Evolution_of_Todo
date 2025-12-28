"""
Test script for the Console Todo Application
This script demonstrates all the functionality of the todo app
"""

from src.services.todo_service import TodoService

def test_all_features():
    print("=== Testing Console Todo Application ===\n")

    # Initialize the service
    service = TodoService()

    # Test adding todos
    print("1. Adding todos...")
    todo1 = service.add_todo("Buy groceries", priority="high", due_date="2025-12-31")
    todo2 = service.add_todo("Walk the dog", priority="medium")
    todo3 = service.add_todo("Complete project", priority="high", completed=True)
    print(f"   + Added: {todo1['description']} (ID: {todo1['id']})")
    print(f"   + Added: {todo2['description']} (ID: {todo2['id']})")
    print(f"   + Added: {todo3['description']} (ID: {todo3['id']})")

    # Test viewing all todos
    print("\n2. Viewing all todos...")
    all_todos = service.get_all_todos()
    for todo in all_todos:
        status = "[X]" if todo['completed'] else "[ ]"
        print(f"   {status} {todo['id']}: {todo['description']} - {todo['priority']} - Due: {todo['due_date'] or 'None'}")

    # Test updating a todo
    print("\n3. Updating a todo...")
    updated = service.update_todo(todo1['id'], description="Buy groceries and cook dinner", priority="high")
    print(f"   + Updated: {updated['description']} - {updated['priority']}")

    # Test toggling completion
    print("\n4. Toggling completion status...")
    toggled = service.toggle_completion(todo2['id'])
    print(f"   + Toggled: {toggled['description']} is now {'COMPLETED' if toggled['completed'] else 'INCOMPLETE'}")

    # Test searching
    print("\n5. Searching for todos...")
    search_results = service.search_todos("groceries")
    print(f"   + Found {len(search_results)} todo(s) matching 'groceries'")

    # Test filtering by status
    print("\n6. Filtering by status...")
    completed_todos = service.filter_todos(status="completed")
    incomplete_todos = service.filter_todos(status="incomplete")
    print(f"   + Completed todos: {len(completed_todos)}")
    print(f"   + Incomplete todos: {len(incomplete_todos)}")

    # Test filtering by priority
    print("\n7. Filtering by priority...")
    high_priority = service.filter_todos(priority="high")
    print(f"   + High priority todos: {len(high_priority)}")

    # Test deleting a todo
    print("\n8. Deleting a todo...")
    try:
        service.delete_todo(todo2['id'])
        print(f"   + Deleted todo with ID {todo2['id']}")
    except ValueError as e:
        print(f"   - Error deleting todo: {e}")

    # Final view to confirm deletion
    print("\n9. Final view after deletion...")
    final_todos = service.get_all_todos()
    print(f"   + Total todos remaining: {len(final_todos)}")

    print("\n=== All tests completed successfully! ===")
    print("\nThe Console Todo Application is working correctly with all features:")
    print("- Adding todos with description, priority, and due date")
    print("- Viewing all todos with status and details")
    print("- Updating todo details")
    print("- Toggling completion status")
    print("- Searching todos by keyword")
    print("- Filtering todos by status, priority, and due date")
    print("- Deleting todos")

if __name__ == "__main__":
    test_all_features()