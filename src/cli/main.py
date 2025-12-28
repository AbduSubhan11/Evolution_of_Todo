'''
Main CLI interface for the Console Todo Application
Implements the console menu system and user interaction
'''

import sys
import os
# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from typing import Optional
from src.services.todo_service import TodoService




class TodoCLI:
    '''
    Command Line Interface for the Todo application
    Provides a menu-driven interface for all todo operations
    '''

    def __init__(self):
        '''
        Initialize the CLI with a TodoService instance
        '''
        self.service = TodoService()
        self.running = True

    def display_menu(self):
        '''
        Display the main menu options to the user
        '''
        print("\n" + "="*50)
        print("           CONSOLE TODO APPLICATION")
        print("="*50)
        print("1. Add Todo")
        print("2. View All Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Todo as Complete/Incomplete")
        print("6. Search Todos")
        print("7. Filter Todos")
        print("8. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        '''
        Get and validate user menu choice

        Returns:
            User's menu choice as a string
        '''
        while True:
            try:
                choice = input("Enter your choice (1-8): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 8.")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                sys.exit(0)
            except EOFError:
                print("\n\nGoodbye!")
                sys.exit(0)

    def add_todo(self):
        '''
        Handle adding a new todo
        '''
        print("\n--- Add New Todo ---")
        try:
            description = input("Enter todo description: ").strip()
            if not description:
                print("Error: Description cannot be empty.")
                return

            priority = input("Enter priority (low/medium/high) [default: medium]: ").strip().lower()
            if priority not in ['low', 'medium', 'high']:
                if priority == '':
                    priority = 'medium'
                else:
                    print("Invalid priority. Using 'medium' as default.")
                    priority = 'medium'

            due_date = input("Enter due date (YYYY-MM-DD) [optional]: ").strip()
            if due_date == '':
                due_date = None

            todo = self.service.add_todo(description, priority, due_date)
            print(f"Todo added successfully with ID: {todo['id']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def view_todos(self):
        '''
        Handle viewing all todos
        '''
        print("\n--- All Todos ---")
        try:
            todos = self.service.get_all_todos()
            if not todos:
                print("No todos found.")
                return

            print(f"{'ID':<3} {'Description':<30} {'Status':<12} {'Priority':<8} {'Due Date':<12}")
            print("-" * 70)
            for todo in todos:
                status = "Complete" if todo['completed'] else "Incomplete"
                due_date = todo['due_date'][:10] if todo['due_date'] else "None"
                description = todo['description'][:27] + "..." if len(todo['description']) > 30 else todo['description']
                print(f"{todo['id']:<3} {description:<30} {status:<12} {todo['priority']:<8} {due_date:<12}")
        except Exception as e:
            print(f"Error retrieving todos: {e}")

    def update_todo(self):
        '''
        Handle updating an existing todo
        '''
        print("\n--- Update Todo ---")
        try:
            todo_id = int(input("Enter todo ID to update: "))
        except ValueError:
            print("Error: Invalid ID. Please enter a number.")
            return

        # Check if todo exists
        all_todos = self.service.get_all_todos()
        todo_exists = any(todo['id'] == todo_id for todo in all_todos)
        if not todo_exists:
            print(f"Error: Todo with ID {todo_id} does not exist.")
            return

        print("Leave fields blank to keep current values.")
        description = input("Enter new description [optional]: ").strip()
        description = description if description else None

        priority = input("Enter new priority (low/medium/high) [optional]: ").strip().lower()
        priority = priority if priority in ['low', 'medium', 'high'] else None

        due_date = input("Enter new due date (YYYY-MM-DD) [optional]: ").strip()
        due_date = due_date if due_date else None

        try:
            updated_todo = self.service.update_todo(todo_id, description, priority, due_date)
            if updated_todo:
                print(f"Todo ID {todo_id} updated successfully.")
            else:
                print(f"Error: Todo with ID {todo_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_todo(self):
        '''
        Handle deleting a todo
        '''
        print("\n--- Delete Todo ---")
        try:
            todo_id = int(input("Enter todo ID to delete: "))
        except ValueError:
            print("Error: Invalid ID. Please enter a number.")
            return

        try:
            self.service.delete_todo(todo_id)
            print(f"Todo ID {todo_id} deleted successfully.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def toggle_completion(self):
        '''
        Handle toggling a todo's completion status
        '''
        print("\n--- Toggle Todo Completion ---")
        try:
            todo_id = int(input("Enter todo ID to toggle: "))
        except ValueError:
            print("Error: Invalid ID. Please enter a number.")
            return

        try:
            result = self.service.toggle_completion(todo_id)
            if result:
                status = "Complete" if result['completed'] else "Incomplete"
                print(f"Todo ID {todo_id} marked as {status}.")
            else:
                print(f"Error: Todo with ID {todo_id} not found.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def search_todos(self):
        '''
        Handle searching todos by keyword
        '''
        print("\n--- Search Todos ---")
        keyword = input("Enter keyword to search: ").strip()
        if not keyword:
            print("Error: Keyword cannot be empty.")
            return

        try:
            todos = self.service.search_todos(keyword)
            if not todos:
                print("No matching todos found.")
                return

            print(f"Search results for '{keyword}':")
            print(f"{'ID':<3} {'Description':<30} {'Status':<12} {'Priority':<8} {'Due Date':<12}")
            print("-" * 70)
            for todo in todos:
                status = "Complete" if todo['completed'] else "Incomplete"
                due_date = todo['due_date'][:10] if todo['due_date'] else "None"
                description = todo['description'][:27] + "..." if len(todo['description']) > 30 else todo['description']
                print(f"{todo['id']:<3} {description:<30} {status:<12} {todo['priority']:<8} {due_date:<12}")
        except Exception as e:
            print(f"Error searching todos: {e}")

    def filter_todos(self):
        '''
        Handle filtering todos by criteria
        '''
        print("\n--- Filter Todos ---")
        print("Leave options blank to skip filtering by that criteria.")

        status = input("Filter by status (completed/incomplete) [optional]: ").strip().lower()
        if status and status not in ['completed', 'incomplete']:
            print("Invalid status. Skipping status filter.")
            status = None

        priority = input("Filter by priority (low/medium/high) [optional]: ").strip().lower()
        if priority and priority not in ['low', 'medium', 'high']:
            print("Invalid priority. Skipping priority filter.")
            priority = None

        due_date = input("Filter by due date (YYYY-MM-DD) [optional]: ").strip()
        if due_date == '':
            due_date = None

        try:
            todos = self.service.filter_todos(status, priority, due_date)
            if not todos:
                print("No matching todos found.")
                return

            print("Filter results:")
            print(f"{'ID':<3} {'Description':<30} {'Status':<12} {'Priority':<8} {'Due Date':<12}")
            print("-" * 70)
            for todo in todos:
                status = "Complete" if todo['completed'] else "Incomplete"
                due_date_str = todo['due_date'][:10] if todo['due_date'] else "None"
                description = todo['description'][:27] + "..." if len(todo['description']) > 30 else todo['description']
                print(f"{todo['id']:<3} {description:<30} {status:<12} {todo['priority']:<8} {due_date_str:<12}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run(self):
        '''
        Main application loop
        '''
        print("Welcome to the Console Todo Application!")
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.add_todo()
            elif choice == '2':
                self.view_todos()
            elif choice == '3':
                self.update_todo()
            elif choice == '4':
                self.delete_todo()
            elif choice == '5':
                self.toggle_completion()
            elif choice == '6':
                self.search_todos()
            elif choice == '7':
                self.filter_todos()
            elif choice == '8':
                print("\nThank you for using the Console Todo Application!")
                self.running = False


def main():
    '''
    Main function to start the application
    '''
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()