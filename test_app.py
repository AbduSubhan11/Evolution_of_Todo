#!/usr/bin/env python3
"""
Test script to verify the console todo application is working properly
"""
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.cli.main import TodoCLI

def test_app_functionality():
    """Test the basic functionality of the TodoCLI application"""
    print("Testing Console Todo Application...")

    # Create an instance of the CLI
    cli = TodoCLI()

    # Test adding a few todos
    print("\n1. Testing Add Todo functionality...")
    try:
        # Simulate adding a todo (we'll call the service directly since we can't simulate user input easily)
        from src.services.todo_service import TodoService
        service = TodoService()

        # Add a few test todos
        todo1 = service.add_todo("Test todo 1", "high", "2025-12-31")
        print(f"   Added todo: {todo1['description']} with ID: {todo1['id']}")

        todo2 = service.add_todo("Test todo 2", "medium")
        print(f"   Added todo: {todo2['description']} with ID: {todo2['id']}")

        todo3 = service.add_todo("Complete project", "high", "2025-01-15", completed=True)
        print(f"   Added todo: {todo3['description']} with ID: {todo3['id']}")

        print("   [PASS] Add Todo functionality works")
    except Exception as e:
        print(f"   [FAIL] Add Todo functionality failed: {e}")
        return False

    # Test viewing all todos
    print("\n2. Testing View All Todos functionality...")
    try:
        todos = service.get_all_todos()
        print(f"   Retrieved {len(todos)} todos")
        for todo in todos:
            status = "Complete" if todo['completed'] else "Incomplete"
            print(f"   - ID: {todo['id']}, Description: {todo['description']}, Status: {status}")
        print("   [PASS] View All Todos functionality works")
    except Exception as e:
        print(f"   [FAIL] View All Todos functionality failed: {e}")
        return False

    # Test updating a todo
    print("\n3. Testing Update Todo functionality...")
    try:
        updated_todo = service.update_todo(todo1['id'], description="Updated test todo", priority="low")
        if updated_todo:
            print(f"   Updated todo ID {updated_todo['id']}: {updated_todo['description']}")
            print("   [PASS] Update Todo functionality works")
        else:
            print("   [FAIL] Update Todo functionality failed - todo not found")
            return False
    except Exception as e:
        print(f"   [FAIL] Update Todo functionality failed: {e}")
        return False

    # Test toggling completion
    print("\n4. Testing Toggle Completion functionality...")
    try:
        toggled_todo = service.toggle_completion(todo2['id'])
        if toggled_todo:
            status = "Complete" if toggled_todo['completed'] else "Incomplete"
            print(f"   Toggled todo ID {toggled_todo['id']} to: {status}")
            print("   [PASS] Toggle Completion functionality works")
        else:
            print("   [FAIL] Toggle Completion functionality failed - todo not found")
            return False
    except Exception as e:
        print(f"   [FAIL] Toggle Completion functionality failed: {e}")
        return False

    # Test searching todos
    print("\n5. Testing Search Todos functionality...")
    try:
        search_results = service.search_todos("test")
        print(f"   Found {len(search_results)} todos matching 'test'")
        for todo in search_results:
            print(f"   - ID: {todo['id']}, Description: {todo['description']}")
        print("   [PASS] Search Todos functionality works")
    except Exception as e:
        print(f"   [FAIL] Search Todos functionality failed: {e}")
        return False

    # Test filtering todos
    print("\n6. Testing Filter Todos functionality...")
    try:
        filtered_todos = service.filter_todos(status="completed")
        print(f"   Found {len(filtered_todos)} completed todos")
        for todo in filtered_todos:
            print(f"   - ID: {todo['id']}, Description: {todo['description']}")
        print("   [PASS] Filter Todos functionality works")
    except Exception as e:
        print(f"   [FAIL] Filter Todos functionality failed: {e}")
        return False

    # Test deleting a todo
    print("\n7. Testing Delete Todo functionality...")
    try:
        service.delete_todo(todo1['id'])
        print(f"   Deleted todo with ID: {todo1['id']}")

        # Verify it's gone
        remaining_todos = service.get_all_todos()
        if not any(todo['id'] == todo1['id'] for todo in remaining_todos):
            print("   [PASS] Delete Todo functionality works")
        else:
            print("   [FAIL] Delete Todo functionality failed - todo still exists")
            return False
    except Exception as e:
        print(f"   [FAIL] Delete Todo functionality failed: {e}")
        return False

    print("\n[SUCCESS] All functionality tests passed!")
    print("The Console Todo Application is working properly.")
    return True

if __name__ == "__main__":
    success = test_app_functionality()
    if not success:
        print("\n[ERROR] Some functionality tests failed.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All tests passed successfully!")