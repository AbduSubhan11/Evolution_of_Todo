// Use the custom shim that interfaces with our existing backend
import { createAuthClient } from './better-auth-client-shim';

// Create the auth client instance using our custom implementation
const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  fetchOptions: {
    credentials: 'include',
  },
});

// Export individual methods
export const { signIn, signUp, signOut, getSession } = authClient;