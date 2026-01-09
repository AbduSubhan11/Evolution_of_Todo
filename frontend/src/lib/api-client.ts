class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
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
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }

  // Authentication endpoints
  async register(email: string, password: string) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('email', email);
    formData.append('password', password);

    return this.request('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });
  }

  async logout(token?: string) {
    return this.request('/api/auth/logout', {
      method: 'POST',
    }, token);
  }

  // Task endpoints
  async getTasks(userId: string, token: string, filters?: { status?: string; limit?: number; offset?: number }) {
    let url = `/api/${userId}/tasks`;
    if (filters) {
      const searchParams = new URLSearchParams();
      if (filters.status) searchParams.append('status', filters.status);
      if (filters.limit) searchParams.append('limit', filters.limit.toString());
      if (filters.offset) searchParams.append('offset', filters.offset.toString());
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