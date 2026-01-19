'use client';

import React, { useState } from 'react';
import { useAuth } from '../../providers/auth-provider';

interface LoginFormProps {
  onLoginSuccess?: () => void;
  onSwitchToRegister?: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { signIn } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await signIn(email, password);
      onLoginSuccess?.();
    } catch (err: any) {
      // Handle specific error messages
      if (err.message.includes('401')) {
        setError('Invalid email or password. Please check your credentials and try again.');
      } else if (err.message.includes('400')) {
        setError('Invalid input. Please check your email and password.');
      } else if (err.message.includes('Network Error')) {
        setError('Unable to connect to the server. Please check your internet connection.');
      } else {
        setError(err.message || 'An error occurred during login. Please try again.');
      }
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-[#1a222a] p-8 rounded-lg border border-[#2d3748]">
      <h2 className="text-2xl font-bold mb-6 text-center text-[#e6e6e6]">Login</h2>

      {error && (
        <div className="mb-4 p-3 bg-red-500/20 text-red-300 rounded-md border border-red-500/50">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-[#a0aec0] mb-2">
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 bg-[#0f1419] border border-[#2d3748] rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-[#e6e6e6]"
            required
          />
        </div>

        <div className="mb-6">
          <label htmlFor="password" className="block text-[#a0aec0] mb-2">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 bg-[#0f1419] border border-[#2d3748] rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-[#e6e6e6]"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <div className="mt-4 text-center">
        <p className="text-[#a0aec0]">
          {'Don&apos;t have an account? '}{' '}
          <button
            onClick={onSwitchToRegister}
            className="text-blue-400 hover:text-blue-300 hover:underline focus:outline-none transition-colors"
          >
            Register here
          </button>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;