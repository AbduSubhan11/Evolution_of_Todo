# Quickstart Guide: Todo AI Chatbot

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.9+ for backend development
- PostgreSQL 12+ (Neon-compatible)
- Better Auth configured for authentication
- OpenAI API key for AI functionality
- Docker (optional, for containerized development)

## Environment Setup

### 1. Clone and Initialize Repository
```bash
git clone <repository-url>
cd <project-root>
npm install  # for frontend
pip install -r requirements.txt  # for backend
```

### 2. Set Up Environment Variables
Create `.env` files for both frontend and backend:

**Frontend (.env.local):**
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_OPENAI_API_KEY=your_openai_key_here
```

**Backend (.env):**
```
OPENAI_API_KEY=your_openai_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWT_SECRET=your_jwt_secret
```

### 3. Database Setup
```bash
# Apply database migrations including new chatbot tables
psql -d todo_db -f migrations/001_create_chat_tables.sql
```

## Development Workflow

### 1. Start Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

### 3. Run Tests
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

## Key Endpoints

### Chat API
- `POST /api/{user_id}/chat` - Main chat endpoint

### MCP Tools (Internal)
- `POST /internal/tools/add_task` - Add a new task
- `GET /internal/tools/list_tasks` - List tasks with filters
- `POST /internal/tools/complete_task` - Complete a task
- `DELETE /internal/tools/delete_task` - Delete a task
- `PUT /internal/tools/update_task` - Update a task

## Database Schema

New tables for chat functionality:
- `conversations` - Stores conversation threads
- `messages` - Stores individual messages
- `task_operation_logs` - Logs task operations performed

## Running the Application

### Development
1. Ensure PostgreSQL is running
2. Start backend server on port 8000
3. Start frontend server on port 3000
4. Access the application at http://localhost:3000

### Testing
1. Run unit tests for both frontend and backend
2. Execute integration tests for chat functionality
3. Verify authentication flow works with Better Auth
4. Test AI interactions with sample natural language commands

## Troubleshooting

### Common Issues
- **Authentication errors**: Verify JWT tokens are properly configured
- **AI service timeouts**: Check OpenAI API key and network connectivity
- **Database connection errors**: Confirm DATABASE_URL is correct
- **CORS errors**: Ensure frontend and backend origins are properly configured

### Debugging Tips
- Enable debug logging in backend with DEBUG=true
- Check browser console for frontend errors
- Monitor API response times and error rates
- Verify conversation state is properly maintained