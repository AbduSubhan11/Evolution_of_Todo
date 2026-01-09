# Data Model: Authentication & API Integration

## Entity: User

**Description**: Represents a registered user in the system with authentication capabilities

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String (255) - User's email address (unique, required)
- `password_hash`: String (255) - Hashed password for authentication
- `created_at`: DateTime - Timestamp when the user account was created
- `updated_at`: DateTime - Timestamp when the user account was last updated
- `is_active`: Boolean - Whether the account is active (default: true)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (8+ characters)
- All required fields must be present

**Relationships**:
- One-to-Many: User has many Tasks (user.tasks)

## Entity: Task

**Description**: Represents a todo item that belongs to a specific authenticated user

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the task
- `title`: String (255) - Title of the task (required)
- `description`: Text - Detailed description of the task (optional)
- `status`: String (20) - Status of the task (enum: pending, completed, archived)
- `user_id`: UUID (Foreign Key) - Reference to the owning user (required)
- `created_at`: DateTime - Timestamp when the task was created
- `updated_at`: DateTime - Timestamp when the task was last updated
- `completed_at`: DateTime - Timestamp when the task was marked as completed (optional)

**Validation Rules**:
- Title must be provided and not empty
- Status must be one of the allowed values (pending, completed, archived)
- User_id must reference an existing user
- All required fields must be present

**Relationships**:
- Many-to-One: Task belongs to one User (task.user)

## Database Schema

**Users Table**:
```
users (
  id: UUID PRIMARY KEY,
  email: VARCHAR(255) UNIQUE NOT NULL,
  password_hash: VARCHAR(255) NOT NULL,
  created_at: TIMESTAMP NOT NULL,
  updated_at: TIMESTAMP NOT NULL,
  is_active: BOOLEAN DEFAULT TRUE
)
```

**Tasks Table**:
```
tasks (
  id: UUID PRIMARY KEY,
  title: VARCHAR(255) NOT NULL,
  description: TEXT,
  status: VARCHAR(20) NOT NULL DEFAULT 'pending',
  user_id: UUID NOT NULL REFERENCES users(id),
  created_at: TIMESTAMP NOT NULL,
  updated_at: TIMESTAMP NOT NULL,
  completed_at: TIMESTAMP
)
```

**Indexes**:
- Index on users.email for fast authentication lookups
- Index on tasks.user_id for efficient user-based filtering
- Index on tasks.status for status-based queries

## State Transitions

**Task Status Transitions**:
- `pending` → `completed` (when user marks task as done)
- `completed` → `pending` (when user unmarks task as done)
- `pending` → `archived` (when user archives task)
- `completed` → `archived` (when user archives completed task)

## Security Considerations

**Data Access**:
- All task queries must be filtered by user_id
- Users cannot access tasks owned by other users
- Authentication required for all data access operations
- Passwords must be stored as secure hashes (bcrypt or similar)

**Constraints**:
- Foreign key constraint ensures referential integrity
- Cascade delete should not be enabled on user deletion to preserve audit trail
- Unique constraint on email prevents duplicate accounts