# API Contracts: Todo Frontend

## Overview

This document outlines the planned API contracts for the Todo application that will be implemented in future phases. For the current frontend-only implementation, these will be mocked using local state management.

## Planned API Endpoints

### Task Management Endpoints

```
GET    /api/{user_id}/tasks          # List all tasks for a user
POST   /api/{user_id}/tasks          # Create a new task
GET    /api/{user_id}/tasks/{id}     # Get task details
PUT    /api/{user_id}/tasks/{id}     # Update a task
DELETE /api/{user_id}/tasks/{id}     # Delete a task
PATCH  /api/{user_id}/tasks/{id}/complete  # Toggle completion
```

### Request/Response Examples

#### Get All Tasks
- **Request**: `GET /api/{user_id}/tasks`
- **Response**:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Optional description",
      "completed": false,
      "createdAt": "2026-01-06T10:00:00Z",
      "updatedAt": "2026-01-06T10:00:00Z"
    }
  ]
}
```

#### Create Task
- **Request**: `POST /api/{user_id}/tasks`
```json
{
  "title": "New task title",
  "description": "Optional description"
}
```
- **Response**: 201 Created with task object

#### Update Task
- **Request**: `PUT /api/{user_id}/tasks/{id}`
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": false
}
```
- **Response**: 200 OK with updated task object

## Current Mock Implementation

For the frontend-only phase, these API calls will be replaced with in-memory state management using React hooks. The service layer will be designed to easily transition to real API calls when the backend is implemented.