'use client';

import React, { useState } from 'react';
import { useAuth } from '../../providers/auth-provider';

interface RegisterFormProps {
  onRegisterSuccess?: () => void;
  onSwitchToLogin?: () => void;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ onRegisterSuccess, onSwitchToLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { signUp } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      setLoading(false);
      return;
    }

    try {
      await signUp(email, password);
      // Redirect to login after successful registration
      onSwitchToLogin?.();
    } catch (err: any) {
      // Handle specific error messages
      if (err.message.includes('409')) {
        setError('Email already exists. Please use a different email address.');
      } else if (err.message.includes('400')) {
        setError('Invalid input. Please check your email and password.');
      } else if (err.message.includes('Network Error')) {
        setError('Unable to connect to the server. Please check your internet connection.');
      } else {
        setError(err.message || 'An error occurred during registration. Please try again.');
      }
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-[#1a222a] p-8 rounded-lg border border-[#2d3748]">
      <h2 className="text-2xl font-bold mb-6 text-center text-[#e6e6e6]">Register</h2>

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

        <div className="mb-4">
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

        <div className="mb-6">
          <label htmlFor="confirmPassword" className="block text-[#a0aec0] mb-2">
            Confirm Password
          </label>
          <input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full px-3 py-2 bg-[#0f1419] border border-[#2d3748] rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-[#e6e6e6]"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>

      <div className="mt-4 text-center">
        <p className="text-[#a0aec0]">
          Already have an account?{' '}
          <button
            onClick={onSwitchToLogin}
            className="text-blue-400 hover:text-blue-300 hover:underline focus:outline-none transition-colors"
          >
            Login here
          </button>
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;