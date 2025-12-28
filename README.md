# Console Todo Application

A simple console-based todo application built with Python that allows users to manage their tasks efficiently.

## Features

- Add new todos with descriptions, priorities, and optional due dates
- View all todos with their status, priority, and due dates
- Update existing todo details
- Delete todos
- Mark todos as complete/incomplete
- Search todos by keyword
- Filter todos by status, priority, or due date

## Requirements

- Python 3.12 or higher

## Installation & Setup

1. Navigate to your project directory:
  
2. Activate the virtual environment:

   ```bash
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Application

**Important**: Make sure your virtual environment is activated before running the application.

### Method 1: Using Python Module Command (Recommended)
```bash
python -m src.cli.main
```

### Method 2: Direct Python Execution
```bash
python src/cli/main.py
```

### Using the Application
Once you run the command, you'll see the main menu:
```
Welcome to the Console Todo Application!
==================================================
           CONSOLE TODO APPLICATION
==================================================
1. Add Todo
2. View All Todos
3. Update Todo
4. Delete Todo
5. Mark Todo as Complete/Incomplete
6. Search Todos
7. Filter Todos
8. Exit
==================================================
```

Follow the on-screen prompts to manage your todos:
- Enter a number (1-8) to select an option
- Follow the specific prompts for each operation
- Press `8` to exit the application

## Project Structure

```
Evolution of Todo App/
├── src/
│   ├── cli/
│   │   └── main.py          # Console interface and menu system
│   ├── models/
│   │   └── todo.py          # Todo entity and TodoList collection
│   └── services/
│       └── todo_service.py  # Business logic for todo operations
├── tests/                   # Comprehensive unit and integration tests using pytest
├── requirements.txt         # Project dependencies
├── pyproject.toml           # Project configuration
├── README.md               # This file
└── .gitignore
```

## Testing

The application includes comprehensive tests that verify all functionality. To run the tests:

```bash
pytest
```

All 67 tests should pass successfully, confirming the application is working correctly.

## Data Model

### Todo
- `id`: Unique identifier (integer)
- `description`: Task description (string)
- `completed`: Completion status (boolean)
- `priority`: Priority level ('low', 'medium', 'high')
- `created_date`: Date when todo was created (datetime)
- `due_date`: Optional due date (datetime or None)

### TodoList
- Collection of Todo items stored in memory
- Provides operations like add, update, delete, search, and filter

## Architecture

The application follows a clear separation of concerns:

- **Models** (`src/models/`): Contains the Todo entity and TodoList collection
- **Services** (`src/services/`): Contains the logics for todo operations eg. Create, Updated, Delete etc
- **CLI** (`src/cli/`): Contains the console interface and user interaction
- **Tests** (`tests/`): Contains comprehensive unit and integration tests "# Evolution_of_Todo" 
