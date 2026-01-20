import React from 'react';
import { useAuth } from '@/providers/auth-provider';
import { useRouter } from 'next/navigation';
import ChatInterface from './ChatInterface';
import ConversationHistory from './ConversationHistory';

interface ProtectedChatRouteProps {
  children?: React.ReactNode;
}

const ProtectedChatRoute: React.FC<ProtectedChatRouteProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  // If loading, show a loading indicator
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If not authenticated, redirect to login or show an error
  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <h2 className="text-xl font-semibold mb-4">Access Denied</h2>
        <p className="text-gray-600 mb-4">Please sign in to use the AI chatbot</p>
        <button
          onClick={() => router.push('/login')}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Sign In
        </button>
      </div>
    );
  }

  // If authenticated, render the chat interface
  return (
    <div className="flex flex-col h-screen max-w-6xl mx-auto">
      <div className="flex flex-1 overflow-hidden">
        <ConversationHistory onSelectConversation={() => {}} />
        <div className="flex-1 p-4">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
};

export default ProtectedChatRoute;