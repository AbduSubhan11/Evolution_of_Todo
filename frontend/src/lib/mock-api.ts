import { Task } from './types';

// In-memory storage for mock data
let mockTasks: Task[] = [
  {
    id: '1',
    title: 'Sample Task',
    description: 'This is a sample task to demonstrate the application',
    completed: false,
    createdAt: new Date(),
    updatedAt: new Date(),
  },
  {
    id: '2',
    title: 'Learn Next.js',
    description: 'Complete the Next.js tutorial',
    completed: true,
    createdAt: new Date(Date.now() - 86400000), // 1 day ago
    updatedAt: new Date(Date.now() - 86400000),
  }
];

// Helper function to generate unique IDs
const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9);
};

// Helper function to convert date to ISO string for consistency
const formatDate = (date: Date): Date => {
  return new Date(date);
};

export const mockApi = {
  // Get all tasks
  getTasks: (): Promise<Task[]> => {
    return new Promise((resolve) => {
      setTimeout(() => resolve([...mockTasks]), 200); // Simulate network delay
    });
  },

  // Create a new task
  createTask: (title: string, description?: string): Promise<Task> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const newTask: Task = {
          id: generateId(),
          title,
          description,
          completed: false,
          createdAt: formatDate(new Date()),
          updatedAt: formatDate(new Date()),
        };
        mockTasks.push(newTask);
        resolve(newTask);
      }, 300); // Simulate network delay
    });
  },

  // Update an existing task
  updateTask: (id: string, updates: Partial<Task>): Promise<Task> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const taskIndex = mockTasks.findIndex(task => task.id === id);
        if (taskIndex === -1) {
          reject(new Error('Task not found'));
          return;
        }

        const updatedTask = {
          ...mockTasks[taskIndex],
          ...updates,
          updatedAt: formatDate(new Date()),
        };

        mockTasks[taskIndex] = updatedTask;
        resolve(updatedTask);
      }, 300); // Simulate network delay
    });
  },

  // Delete a task
  deleteTask: (id: string): Promise<boolean> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const initialLength = mockTasks.length;
        mockTasks = mockTasks.filter(task => task.id !== id);

        if (mockTasks.length === initialLength) {
          reject(new Error('Task not found'));
          return;
        }

        resolve(true);
      }, 300); // Simulate network delay
    });
  },

  // Toggle task completion status
  toggleTaskCompletion: (id: string): Promise<Task> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const taskIndex = mockTasks.findIndex(task => task.id === id);
        if (taskIndex === -1) {
          reject(new Error('Task not found'));
          return;
        }

        const updatedTask = {
          ...mockTasks[taskIndex],
          completed: !mockTasks[taskIndex].completed,
          updatedAt: formatDate(new Date()),
        };

        mockTasks[taskIndex] = updatedTask;
        resolve(updatedTask);
      }, 300); // Simulate network delay
    });
  },
};