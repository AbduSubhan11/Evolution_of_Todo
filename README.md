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

For Manually Run
cd backend && python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

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

# Phase 2: Evolution to Full Stack Web Application

## Overview
The console-based todo application has evolved into a modern full-stack web application featuring user authentication, a responsive UI, and cloud database storage.

## New Features
- **User Authentication System**: Secure JWT-based authentication with login/register functionality
- **Modern Web Interface**: Built with Next.js for a responsive and intuitive user experience
- **Cloud Database**: User data stored in Neon PostgreSQL database for scalability
- **API Endpoints**: RESTful API with endpoints for user management and todo operations
- **Task Management**: Enhanced task features with status tracking, filtering, and management

## Technology Stack
- **Frontend**: Next.js 14+, React, TypeScript
- **Backend**: FastAPI with Python
- **Database**: Neon PostgreSQL
- **Authentication**: Custom JWT implementation
- **ORM**: SQLModel for database operations
- **Styling**: Tailwind CSS

## Project Structure (Updated)
```
Evolution of Todo App/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── auth/           # Authentication logic
│   │   ├── models/         # Data models (User, Task)
│   │   ├── database/       # Database configuration
│   │   ├── middleware/     # Authentication middleware
│   │   └── main.py         # Main application entry point
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js app router pages
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/            # API client and utilities
│   │   └── providers/      # Context providers (Auth)
│   ├── package.json
│   └── tailwind.config.js
├── src/                     # Original console app (Phase 1)
│   ├── cli/
│   ├── models/
│   └── services/
├── README.md               # This file
└── .env                    # Environment variables
```

## How to Run Phase 2 (Full Stack Application)

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Neon database URL and JWT secret
```

5. Run the backend server:
```bash
python -m uvicorn src.main:app --reload --port 8001
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit NEXT_PUBLIC_API_BASE_URL to match your backend URL
```

4. Run the development server:
```bash
npm run dev
```

The application will be accessible at http://localhost:3000 with the API running on http://localhost:8001.

## API Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/{userId}/tasks` - Get user tasks
- `POST /api/{userId}/tasks` - Create new task
- `PUT /api/{userId}/tasks/{taskId}` - Update task
- `DELETE /api/{userId}/tasks/{taskId}` - Delete task
- `PATCH /api/{userId}/tasks/{taskId}/complete` - Toggle task completion

## Database Schema
- **users** table: Stores user information (id, email, password_hash, timestamps)
- **tasks** table: Stores task information (id, title, description, status, user_id, timestamps)
