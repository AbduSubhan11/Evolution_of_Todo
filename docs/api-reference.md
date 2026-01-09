# API Reference for Todo App

## Authentication Endpoints

### POST /api/auth/register
Register a new user account

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Responses:**
- `201 Created`: User successfully registered
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```
- `400 Bad Request`: Invalid input data
- `409 Conflict`: Email already exists

### POST /api/auth/login
Authenticate user and return JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Responses:**
- `200 OK`: Authentication successful
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  },
  "token": "jwt-token-string"
}
```
- `401 Unauthorized`: Invalid credentials

### POST /api/auth/logout
Invalidate user session

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Responses:**
- `200 OK`: Successfully logged out
```json
{
  "message": "Successfully logged out"
}
```

## Todo Management Endpoints

### GET /api/{user_id}/tasks
Get all tasks for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Path Parameters:**
- `user_id`: User ID from JWT token (validation required)

**Query Parameters:**
- `status`: Filter by status (optional: pending, completed, archived)
- `limit`: Number of results to return (optional)
- `offset`: Number of results to skip (optional)

**Responses:**
- `200 OK`: Successfully retrieved tasks
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "status": "pending",
      "created_at": "2026-01-06T10:00:00Z",
      "updated_at": "2026-01-06T10:00:00Z",
      "completed_at": "2026-01-06T10:00:00Z" // optional
    }
  ],
  "total": 10
}
```
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User trying to access another user's tasks

### POST /api/{user_id}/tasks
Create a new task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Path Parameters:**
- `user_id`: User ID from JWT token (validation required)

**Request:**
```json
{
  "title": "New task title",
  "description": "Task description (optional)",
  "status": "pending" // default if not provided
}
```

**Responses:**
- `201 Created`: Task successfully created
```json
{
  "id": "uuid-string",
  "title": "New task title",
  "description": "Task description",
  "status": "pending",
  "user_id": "user-id-from-token",
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T10:00:00Z"
}
```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User trying to create task for another user

### GET /api/{user_id}/tasks/{id}
Get a specific task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Path Parameters:**
- `user_id`: User ID from JWT token
- `id`: Task ID

**Responses:**
- `200 OK`: Task found
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "user_id": "user-id",
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T10:00:00Z",
  "completed_at": "2026-01-06T10:00:00Z" // optional
}
```
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User trying to access another user's task
- `404 Not Found`: Task not found

### PUT /api/{user_id}/tasks/{id}
Update a specific task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Path Parameters:**
- `user_id`: User ID from JWT token
- `id`: Task ID

**Request:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "completed"
}
```

**Responses:**
- `200 OK`: Task successfully updated
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated task description",
  "status": "completed",
  "user_id": "user-id-from-token",
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T11:00:00Z",
  "completed_at": "2026-01-06T11:00:00Z" // if status is completed
}
```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User trying to update another user's task
- `404 Not Found`: Task not found

### DELETE /api/{user_id}/tasks/{id}
Delete a specific task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Path Parameters:**
- `user_id`: User ID from JWT token
- `id`: Task ID

**Responses:**
- `200 OK`: Task successfully deleted
```json
{
  "message": "Task deleted successfully"
}
```
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User trying to delete another user's task
- `404 Not Found`: Task not found

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle completion status of a task

**Headers:**
```
Authorization: Bearer {jwt-token}
```

**Path Parameters:**
- `user_id`: User ID from JWT token
- `id`: Task ID

**Request:**
```json
{
  "complete": true // or false to unmark
}
```

**Responses:**
- `200 OK`: Task status successfully updated
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "status": "completed", // or "pending"
  "completed_at": "2026-01-06T10:00:00Z" // if completed, null if unmarked
}
```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User trying to modify another user's task
- `404 Not Found`: Task not found

## Error Response Format

All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details (optional)"
  }
}
```

## Common Error Codes

- `UNAUTHORIZED`: 401 - Invalid or missing authentication token
- `FORBIDDEN`: 403 - User not authorized to access this resource
- `NOT_FOUND`: 404 - Requested resource not found
- `VALIDATION_ERROR`: 400 - Request data validation failed
- `CONFLICT`: 409 - Request conflicts with existing data
- `INTERNAL_ERROR`: 500 - Server error occurred