import { Task, TaskFilter } from './types';

// Filter tasks based on the current filter and search query
export const filterTasks = (
  tasks: Task[],
  filter: TaskFilter,
  searchQuery: string
): Task[] => {
  let filteredTasks = [...tasks];

  // Apply status filter
  if (filter === 'completed') {
    filteredTasks = filteredTasks.filter(task => task.status === 'completed');
  } else if (filter === 'pending') {
    filteredTasks = filteredTasks.filter(task => task.status === 'pending');
  }

  // Apply search query filter
  if (searchQuery) {
    const query = searchQuery.toLowerCase();
    filteredTasks = filteredTasks.filter(
      task =>
        task.title.toLowerCase().includes(query) ||
        (task.description && task.description.toLowerCase().includes(query))
    );
  }

  return filteredTasks;
};

// Format date for display
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

// Generate a unique ID
export const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9);
};

// Create a compatibility wrapper for API tasks
export const createTaskCompatibilityWrapper = (apiTask: any) => {
  return {
    ...apiTask,
    get completed() {
      return apiTask.status === 'completed';
    },
    get createdAt() {
      return new Date(apiTask.created_at);
    },
    get updatedAt() {
      return new Date(apiTask.updated_at);
    }
  };
};