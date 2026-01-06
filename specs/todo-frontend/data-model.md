# Data Model: Todo Frontend

## Task Entity

**Name**: Task
**Description**: Represents a user's todo item with properties for title, description, status, and creation date.

**Fields**:
- `id` (string): Unique identifier for the task (UUID format)
- `title` (string): The main text/description of the task (required, 1-200 characters)
- `description` (string): Optional detailed description of the task (0-1000 characters)
- `completed` (boolean): Status indicating if the task is completed (default: false)
- `createdAt` (Date): Timestamp when the task was created
- `updatedAt` (Date): Timestamp when the task was last updated

**Validation Rules**:
- Title must be 1-200 characters
- Title cannot be empty or only whitespace
- Description must be 0-1000 characters if provided
- Completed status must be a boolean value
- createdAt and updatedAt must be valid ISO date strings

**State Transitions**:
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user unmarks completed task

## Task List Entity

**Name**: TaskList
**Description**: Collection of tasks displayed to the user with filtering and sorting capabilities.

**Fields**:
- `tasks` (Task[]): Array of Task entities
- `filter` (string): Current filter state (all, completed, pending)
- `searchQuery` (string): Current search query for filtering tasks

**Validation Rules**:
- tasks array must contain only valid Task entities
- filter must be one of: 'all', 'completed', 'pending'
- searchQuery must be 0-100 characters

## TypeScript Interface Definitions

```typescript
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}

type TaskFilter = 'all' | 'completed' | 'pending';

interface TaskList {
  tasks: Task[];
  filter: TaskFilter;
  searchQuery: string;
}
```

## Mock Data Structure

For the frontend-only implementation, the data will be stored in-memory using React state management:

```typescript
interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}
```

This structure will later be replaced with API integration in future phases.