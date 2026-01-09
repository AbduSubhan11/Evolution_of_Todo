'use client';

import React from 'react';
import { AuthProvider } from '@/providers/auth-provider';

export function Providers({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}