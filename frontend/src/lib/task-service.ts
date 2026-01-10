import { apiClient } from './api-client';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed' | 'archived';
  user_id: string;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
}

interface TaskFilters {
  search?: string;
  status?: 'pending' | 'completed' | 'archived';
  completed?: boolean;
  date_from?: string;
  date_to?: string;
  limit?: number;
  offset?: number;
  sort_by?: string;
  sort_order?: string;
}

class TaskService {
  async getTasks(userId: string, token: string, filters?: TaskFilters): Promise<Task[]> {
    return await apiClient.getTasks(userId, token, filters) as Task[];
  }

  async createTask(userId: string, taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at' | 'completed_at'>, token: string): Promise<Task> {
    return await apiClient.createTask(userId, taskData, token) as Task;
  }

  async getTask(userId: string, taskId: string, token: string): Promise<Task> {
    return await apiClient.getTask(userId, taskId, token) as Task;
  }

  async updateTask(userId: string, taskId: string, taskData: Partial<Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>>, token: string): Promise<Task> {
    return await apiClient.updateTask(userId, taskId, taskData, token) as Task;
  }

  async deleteTask(userId: string, taskId: string, token: string): Promise<void> {
    await apiClient.deleteTask(userId, taskId, token);
  }

  async toggleTaskCompletion(userId: string, taskId: string, complete: boolean, token: string): Promise<Task> {
    return await apiClient.toggleTaskCompletion(userId, taskId, complete, token) as Task;
  }
}

export const taskService = new TaskService();
export type { Task, TaskFilters };