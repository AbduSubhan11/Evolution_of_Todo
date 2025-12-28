# Quickstart: Console Todo Application

## Prerequisites
- Python 3.12+ installed
- uv package manager installed

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment using uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies (if any):
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Application
```bash
python src/cli/main.py
```

## Basic Usage
1. The application starts with a console menu
2. Select options by entering the corresponding number
3. Follow the prompts to add, view, update, delete, or mark todos
4. Use the search/filter option to find specific todos

## Available Commands
- Add Todo: Create a new todo with description, priority, and optional due date
- View Todos: Display all todos with their status
- Update Todo: Modify an existing todo's details
- Delete Todo: Remove a todo from the list
- Mark Complete/Incomplete: Toggle the completion status of a todo
- Search & Filter: Find todos by keyword, status, priority, or date
- Exit: Quit the application