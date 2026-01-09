'use client';

import RegisterForm from '@/components/auth/register-form';
import { useAuth } from '@/providers/auth-provider';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function RegisterPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/'); // Redirect to home if already logged in
    }
  }, [isAuthenticated, router]);

  if (isAuthenticated) {
    return null; // Or a loading indicator while redirecting
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f1419] py-12 px-4 sm:px-6 lg:px-8">
      <RegisterForm
        onRegisterSuccess={() => router.push('/')}
        onSwitchToLogin={() => router.push('/login')}
      />
    </div>
  );
}