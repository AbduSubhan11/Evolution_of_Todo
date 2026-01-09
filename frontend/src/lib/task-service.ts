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
  status?: 'pending' | 'completed' | 'archived';
  limit?: number;
  offset?: number;
}

class TaskService {
  async getTasks(userId: string, token: string, filters?: TaskFilters): Promise<Task[]> {
    return apiClient.getTasks(userId, token, filters);
  }

  async createTask(userId: string, taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at' | 'completed_at'>, token: string): Promise<Task> {
    return apiClient.createTask(userId, taskData, token);
  }

  async getTask(userId: string, taskId: string, token: string): Promise<Task> {
    return apiClient.getTask(userId, taskId, token);
  }

  async updateTask(userId: string, taskId: string, taskData: Partial<Task>, token: string): Promise<Task> {
    return apiClient.updateTask(userId, taskId, taskData, token);
  }

  async deleteTask(userId: string, taskId: string, token: string): Promise<void> {
    return apiClient.deleteTask(userId, taskId, token);
  }

  async toggleTaskCompletion(userId: string, taskId: string, complete: boolean, token: string): Promise<Task> {
    return apiClient.toggleTaskCompletion(userId, taskId, complete, token);
  }
}

export const taskService = new TaskService();
export type { Task, TaskFilters };