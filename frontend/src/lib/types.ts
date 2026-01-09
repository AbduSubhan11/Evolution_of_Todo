export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed' | 'archived';
  user_id: string;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
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