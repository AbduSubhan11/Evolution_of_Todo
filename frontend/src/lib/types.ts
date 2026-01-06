export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export type TaskFilter = 'all' | 'completed' | 'pending';

export interface TaskListState {
  tasks: Task[];
  filter: TaskFilter;
  searchQuery: string;
}

export interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}