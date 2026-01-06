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
    filteredTasks = filteredTasks.filter(task => task.completed);
  } else if (filter === 'pending') {
    filteredTasks = filteredTasks.filter(task => !task.completed);
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
export const formatDate = (date: Date): string => {
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