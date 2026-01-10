class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'; // Backend API for tasks
  }

  // Get headers with authorization
  private getHeaders(token?: string): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Generic request method
  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    token?: string
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const config: RequestInit = {
      headers: {
        ...this.getHeaders(token),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        // Try to get error data from response
        let errorData;
        try {
          errorData = await response.json();
        } catch (e) {
          // If response is not JSON, create a generic error
          errorData = { message: `HTTP error! status: ${response.status}` };
        }

        throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }

  // Authentication is now handled by Better Auth
  // These methods are no longer needed since AuthProvider uses Better Auth directly
  // Keeping them for potential future use if needed

  // Task endpoints
  async getTasks(userId: string, token: string, filters?: {
    search?: string;
    status?: string;
    completed?: boolean;
    date_from?: string;
    date_to?: string;
    limit?: number;
    offset?: number;
    sort_by?: string;
    sort_order?: string;
  }) {
    let url = `/api/${userId}/tasks`;
    if (filters) {
      const searchParams = new URLSearchParams();
      if (filters.search) searchParams.append('search', filters.search);
      if (filters.status) searchParams.append('status_filter', filters.status);
      if (filters.completed !== undefined) searchParams.append('completed', filters.completed.toString());
      if (filters.date_from) searchParams.append('date_from', filters.date_from);
      if (filters.date_to) searchParams.append('date_to', filters.date_to);
      if (filters.limit) searchParams.append('limit', filters.limit.toString());
      if (filters.offset) searchParams.append('offset', filters.offset.toString());
      if (filters.sort_by) searchParams.append('sort_by', filters.sort_by);
      if (filters.sort_order) searchParams.append('sort_order', filters.sort_order);
      url += `?${searchParams.toString()}`;
    }
    return this.request(url, {}, token);
  }

  async createTask(userId: string, taskData: { title: string; description?: string; status?: string }, token: string) {
    return this.request(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    }, token);
  }

  async getTask(userId: string, taskId: string, token: string) {
    return this.request(`/api/${userId}/tasks/${taskId}`, {}, token);
  }

  async updateTask(userId: string, taskId: string, taskData: Partial<{ title: string; description?: string; status?: string }>, token: string) {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }, token);
  }

  async deleteTask(userId: string, taskId: string, token: string) {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    }, token);
  }

  async toggleTaskCompletion(userId: string, taskId: string, complete: boolean, token: string) {
    return this.request(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ complete }),
    }, token);
  }
}

export const apiClient = new ApiClient();