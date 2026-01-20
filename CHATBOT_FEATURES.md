# AI Chatbot Task Management Features

## Overview
The todo app now includes an AI chatbot that can help users manage their tasks through natural language commands. The chatbot leverages Google Gemini AI to understand user requests and performs the appropriate task operations.

## Key Features

### 1. Task Creation
- **Commands**: "Add a task to buy groceries", "Create a task called 'walk the dog'"
- **Supports**: Quoted titles, natural language parsing
- **Function**: Adds new tasks to the user's personal task list

### 2. Task Listing
- **Commands**: "Show me my tasks", "List my completed tasks", "What are my pending tasks?"
- **Filters**: Supports filtering by status (pending, completed, archived)
- **Function**: Retrieves and displays user's tasks

### 3. Task Completion
- **Commands**: "Complete the task 'buy groceries'", "Mark 'walk the dog' as done"
- **Flexible Matching**: Can match by partial title if exact match not found
- **Function**: Updates task status to "completed"

### 4. Task Deletion
- **Commands**: "Delete the task 'buy groceries'", "Remove 'walk the dog' task"
- **Safe Operation**: Verifies user ownership before deletion
- **Function**: Removes tasks from user's list

### 5. Task Updates
- **Commands**: "Update 'buy groceries' to 'buy groceries and cook dinner'"
- **Flexible Matching**: Can update based on partial title matches
- **Function**: Modifies task title and/or description

## Security & Privacy
- **User Isolation**: Each user can only access and manage their own tasks
- **Authentication**: JWT-based authentication ensures secure access
- **Permission Checking**: All operations verify user ownership of tasks

## Technical Implementation

### AI Command Recognition
The AI client uses sophisticated regex patterns to identify user intentions:
- Natural language processing for task creation
- Flexible title matching for task operations
- Status filtering for listing tasks

### Tool Functions
- **add_task**: Creates new tasks with title and optional description
- **list_tasks**: Retrieves tasks with optional status filtering
- **complete_task**: Marks tasks as completed
- **delete_task**: Removes tasks from user's list
- **update_task**: Modifies task details

### Error Handling
- Graceful handling of malformed requests
- Clear error messages for invalid operations
- Safe fallbacks when exact matches aren't found

## Usage Examples

### Adding Tasks
- "Add a task to buy milk"
- "Create a task called 'finish project proposal'"
- "Add task 'call mom' to my list"

### Managing Tasks
- "Show me my tasks" - Lists all tasks
- "List my completed tasks" - Shows only completed tasks
- "Complete the task 'buy milk'" - Marks specific task as done
- "Delete 'finish project proposal'" - Removes task
- "Update 'buy milk' to 'buy milk and bread'" - Changes task title

## Architecture
- **Frontend**: React-based chat interface integrated into the main app
- **Backend**: FastAPI with SQLModel for database operations
- **AI**: Google Gemini integration for natural language processing
- **Database**: Neon PostgreSQL with proper user isolation
- **Authentication**: JWT-based user verification

## Benefits
- **Natural Interaction**: Users can speak naturally to manage tasks
- **Efficiency**: Quick task management without navigating UI
- **Personalization**: Each user has isolated task management
- **Flexibility**: Support for various command phrasings
- **Security**: Robust authentication and authorization