'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { apiClient } from '@/lib/api-client';
import { signIn as betterSignIn, signUp as betterSignUp, signOut as betterSignOut, getSession } from '@/lib/better-auth-client';

interface BetterAuthUser {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}

interface AuthContextType {
  user: BetterAuthUser | null;
  token: string | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<any>;
  signOut: () => Promise<void>;
  signUp: (email: string, password: string) => Promise<any>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<BetterAuthUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on initial load using Better Auth
    const checkSession = async () => {
      try {
        const session = await getSession();
        if (session && session.data && session.data.user) {
          // Transform Better Auth user to our format
          const betterAuthUser = {
            id: session.data.user.id,
            email: session.data.user.email,
            name: session.data.user.name,
            createdAt: session.data.user.createdAt || new Date().toISOString(),
            updatedAt: session.data.user.updatedAt || new Date().toISOString(),
          };

          setUser(betterAuthUser);
          return;
        }

        // Fallback: some setups store a token and user email in localStorage.
        // If the server session is not available but the client has a token, use that
        // to restore a minimal authenticated state (not a substitute for a real session).
        // For proper user ID, we'll rely on the backend session endpoint which returns the UUID.
        try {
          const tokenFromStorage = localStorage.getItem('token');
          const emailFromStorage = localStorage.getItem('email');
          if (tokenFromStorage && emailFromStorage) {
            // We need to call the session endpoint to get the proper user ID
            // Instead of using email as ID, we'll make a call to get the real user info
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/auth/session`, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${tokenFromStorage}`,
                'Content-Type': 'application/json',
              },
            });

            if (res.ok) {
              const userData = await res.json();
              // Use the actual user ID from the backend
              setUser({
                id: userData.id, // This should be the UUID
                email: userData.email,
                name: userData.name,
                createdAt: userData.created_at || new Date().toISOString(),
                updatedAt: userData.updated_at || new Date().toISOString(),
              });
            } else {
              // If session endpoint fails, we still have the token and email
              // but we don't have the proper UUID, so we'll need to handle this carefully
              // In this case, we should not set the user as we don't have the proper ID
              console.warn('Session endpoint failed, unable to get proper user ID');
            }
            setToken(tokenFromStorage);
            return;
          }
        } catch (e) {
          // localStorage may not be available in some environments (shouldn't happen in browser)
          console.warn('Could not read from localStorage to restore session', e);
        }
      } catch (error) {
        console.error('Failed to get session:', error);
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const handleSignIn = async (email: string, password: string) => {
    try {
      // Use Better Auth's sign-in
      const result = await betterSignIn.email({
        email,
        password,
        callbackURL: '/', // Redirect after sign in
      });

      if (result?.error) {
        throw new Error(result.error.message || 'Login failed');
      }

      // Get the updated session
      const session = await getSession();
      if (session && session.data && session.data.user) {
        const betterAuthUser = {
          id: session.data.user.id,
          email: session.data.user.email,
          name: session.data.user.name,
          createdAt: session.data.user.createdAt || new Date().toISOString(),
          updatedAt: session.data.user.updatedAt || new Date().toISOString(),
        };

        setUser(betterAuthUser);
      } else {
        // If no server session is available, but the backend/client stored a token/email in localStorage,
        // restore a minimal authenticated state from that info so refreshes don't kick the user out.
        try {
          const tokenFromStorage = localStorage.getItem('token');
          const emailFromStorage = localStorage.getItem('email');
          if (tokenFromStorage && emailFromStorage) {
            setToken(tokenFromStorage);
            setUser({
              id: emailFromStorage,
              email: emailFromStorage,
              name: undefined,
              createdAt: new Date().toISOString(),
              updatedAt: new Date().toISOString(),
            });
          }
        } catch (e) {
          console.warn('Could not read from localStorage after sign in', e);
        }
      }

      return result;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const handleSignOut = async () => {
    try {
      await betterSignOut();

      // Clear state
      setUser(null);
      setToken(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const handleSignUp = async (email: string, password: string) => {
    try {
      // Use Better Auth's sign-up
      const result = await betterSignUp.email({
        email,
        password,
        name: email.split('@')[0], // Use part of email as name
      });

      if (result?.error) {
        throw new Error(result.error.message || 'Registration failed');
      }

      // Get the updated session
      const session = await getSession();
      if (session && session.data && session.data.user) {
        const betterAuthUser = {
          id: session.data.user.id,
          email: session.data.user.email,
          name: session.data.user.name,
          createdAt: session.data.user.createdAt || new Date().toISOString(),
          updatedAt: session.data.user.updatedAt || new Date().toISOString(),
        };

        setUser(betterAuthUser);
      }

      return result;
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    token,
    loading,
    signIn: handleSignIn,
    signOut: handleSignOut,
    signUp: handleSignUp,
    isAuthenticated: !!user
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};