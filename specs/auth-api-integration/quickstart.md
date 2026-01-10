# Quickstart Guide: Authentication & API Integration

## Prerequisites

- Node.js 18+ for Next.js frontend
- Python 3.12+ for FastAPI backend
- uv package manager (as specified in constitution)
- Neon Serverless PostgreSQL database instance

## Environment Setup

### Frontend (Next.js)
1. Install dependencies:
```bash
npm install @better-auth/react @better-auth/next-js
```

### Backend (FastAPI)
1. Install dependencies:
```bash
uv pip install fastapi sqlmodel pydantic python-jose[cryptography] python-multipart
```

2. Set up environment variables:
```
SECRET_KEY=your-jwt-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
NEON_DATABASE_URL=your-neon-database-url
```

## Key Implementation Files

### Frontend
- `app/providers/auth-provider.tsx` - Better Auth provider setup
- `lib/auth-utils.ts` - Authentication utilities and hooks
- `lib/api-client.ts` - API client with JWT token management

### Backend
- `auth/security.py` - JWT token utilities and validation
- `auth/routers.py` - Authentication endpoints
- `models/user.py` - User SQLModel definition
- `models/task.py` - Task SQLModel definition
- `api/v1/endpoints/tasks.py` - Task CRUD endpoints with user filtering

## Running the Application

### Frontend
```bash
npm run dev
```

### Backend
```bash
uvicorn main:app --reload --port 8000
```

## Testing the Integration

1. Register a new user via POST /api/auth/register
2. Login to get JWT token via POST /api/auth/login
3. Use the token to access user-specific tasks at GET /api/{user_id}/tasks
4. Verify that users cannot access other users' tasks

## Security Notes

- JWT tokens should be stored securely on the frontend
- All API requests require Authorization header with Bearer token
- Database queries always filter by authenticated user ID
- Passwords are hashed using bcrypt before storage