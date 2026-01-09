'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { apiClient } from '@/lib/api-client';

interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
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
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on initial load
    const storedToken = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser && storedUser !== 'undefined') {
      try {
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser && typeof parsedUser === 'object') {
          setToken(storedToken);
          setUser(parsedUser);
        }
      } catch (error) {
        console.error('Failed to parse stored user:', error);
        // Clear invalid stored data
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const handleSignIn = async (email: string, password: string) => {
    try {
      const data = await apiClient.login(email, password);

      // Store token and user info
      const { user, token } = data;
      localStorage.setItem('access_token', token);
      localStorage.setItem('user', JSON.stringify(user));

      setToken(token);
      setUser(user);

      return data;
    } catch (error) {
      console.error('Sign in error:', error);
      if (error instanceof SyntaxError) {
        throw new Error('Invalid response from server. Please try again.');
      }
      throw error;
    }
  };

  const handleSignOut = async () => {
    try {
      // Call backend logout endpoint if needed
      if (token) {
        await apiClient.logout(token);
      }

      // Clear local storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');

      setToken(null);
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const handleSignUp = async (email: string, password: string) => {
    try {
      const data = await apiClient.register(email, password);

      // Store token and user info
      const { user, token } = data;
      localStorage.setItem('access_token', token);
      localStorage.setItem('user', JSON.stringify(user));

      setToken(token);
      setUser(user);

      return data;
    } catch (error) {
      console.error('Sign up error:', error);
      if (error instanceof SyntaxError) {
        throw new Error('Invalid response from server. Please try again.');
      }
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