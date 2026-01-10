export interface CreateAuthClientOptions {
  baseURL?: string;
  fetchOptions?: RequestInit;
}

type SignInParams = { email: string; password: string; callbackURL?: string };
type SignUpParams = { email: string; password: string; name?: string };

function defaultFetch(input: RequestInfo, init?: RequestInit) {
  return fetch(input, init);
}

export function createAuthClient(opts: CreateAuthClientOptions = {}) {
  const baseURL = opts.baseURL ?? process.env.NEXT_PUBLIC_BETTER_AUTH_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8001';
  const fetchOptions = opts.fetchOptions ?? { credentials: 'include' };

  return {
    signIn: {
      email: async ({ email, password, callbackURL }: SignInParams) => {
        try {
          // Use the actual backend login endpoint (with /api prefix)
          const res = await defaultFetch(`${baseURL}/api/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ email, password }),
            ...fetchOptions,
          });

          if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            return { error: errorData, data: undefined };
          }

          const data = await res.json();
          // Store token in localStorage for session persistence
          if (data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('email', data.user?.email || '');
          }
          return { data };
        } catch (error: any) {
          return { error };
        }
      },
    },

    signUp: {
      email: async ({ email, password, name }: SignUpParams) => {
        try {
          // Use the actual backend register endpoint (with /api prefix)
          const res = await defaultFetch(`${baseURL}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
            ...fetchOptions,
          });

          if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            return { error: errorData, data: undefined };
          }

          const data = await res.json();
          // Store token in localStorage for session persistence
          if (data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('email', data.user?.email || '');
          }
          return { data };
        } catch (error: any) {
          return { error };
        }
      },
    },

    signOut: async () => {
      try {
        // Use the actual backend logout endpoint (with /api prefix)
        const res = await defaultFetch(`${baseURL}/api/auth/logout`, {
          method: 'POST',
          ...fetchOptions,
        });

        // Clear stored token and email
        localStorage.removeItem('token');
        localStorage.removeItem('email');

        const data = await res.json().catch(() => ({}));
        if (!res.ok) return { error: data };
        return { error: undefined };
      } catch (error: any) {
        return { error };
      }
    },

    getSession: async () => {
      try {
        // Check if we have a token in localStorage first
        const token = localStorage.getItem('token');
        if (!token) {
          return { data: null, error: { detail: 'No token found' } };
        }

        // Use the actual backend session endpoint (with /api prefix)
        const res = await defaultFetch(`${baseURL}/api/auth/session`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          ...fetchOptions,
        });

        if (!res.ok) {
          const errorData = await res.json().catch(() => ({}));
          // If session is invalid, clear stored credentials
          if (res.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('email');
          }
          return { data: null, error: errorData };
        }

        const data = await res.json();
        return { data, error: undefined };
      } catch (error: any) {
        return { data: null, error };
      }
    },
  };
}

export default createAuthClient;
