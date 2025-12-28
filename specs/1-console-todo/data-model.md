# Data Model: Console Todo Application

## Todo Entity

**Attributes:**
- `id`: Unique identifier (integer or string)
- `description`: Task description (string)
- `completed`: Completion status (boolean)
- `priority`: Priority level (string: 'low', 'medium', 'high')
- `created_date`: Date when todo was created (datetime)
- `due_date`: Optional due date (datetime or None)

**Validation Rules:**
- `description` must not be empty
- `completed` must be boolean
- `priority` must be one of 'low', 'medium', 'high'
- `id` must be unique within the collection

## TodoList Collection

**Attributes:**
- `todos`: List/array of Todo entities
- `next_id`: Counter for generating unique IDs (integer)

**Operations:**
- Add a new Todo
- Remove a Todo by ID
- Update a Todo by ID
- Find Todos by various criteria (keyword, status, priority, date)
- Get all Todos

**State Transitions:**
- Todo can transition from incomplete to complete and vice versa
- Todo can be added to the collection
- Todo can be removed from the collection
- Todo details can be updated while maintaining its ID

## Relationships
- TodoList contains multiple Todo entities
- Each Todo has a unique ID within its TodoList