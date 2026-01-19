'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/providers/auth-provider'; // Using better-auth provider
import { sendMessage } from '@/lib/chatService'; // We'll create this service

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  tool_calls?: any[];
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user, token, isAuthenticated } = useAuth(); // Using better-auth context

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || !isAuthenticated || !user?.id || !token || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    // Add user message to the chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the chat API with token
      const response = await sendMessage(inputValue, user.id as string, token);

      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        content: response.response,
        sender: 'ai',
        timestamp: new Date(),
        tool_calls: response.tool_calls,
      };

      // Add AI response to the chat
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error processing your request.',
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#1a222a] text-[#e6e6e6] rounded-lg">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[300px]">
        {messages.length === 0 ? (
          <div className="text-center text-[#a0aec0] mt-8">
            <p>Start a conversation to manage your tasks!</p>
            <p className="text-sm mt-2">{'Try saying: "Add a task to buy groceries"'}</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-[#2d3748] text-[#e6e6e6]'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                {message.tool_calls && message.tool_calls.length > 0 && (
                  <div className="mt-2 text-xs opacity-75">
                    <p>Tools used:</p>
                    {message.tool_calls.map((tool, index) => (
                      <span key={index} className="inline-block bg-[#4a5568] rounded px-2 py-1 mr-2 text-xs">
                        {tool.function?.name}
                      </span>
                    ))}
                  </div>
                )}
                <div className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-[#2d3748] text-[#e6e6e6] px-4 py-2 rounded-lg max-w-xs">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-[#a0aec0] rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-[#a0aec0] rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-[#a0aec0] rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="border-t border-[#2d3748] py-4 px-4">
        <div className="flex gap-2 ">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your task request..."
            className="flex-1 bg-[#2d3748] text-[#e6e6e6] border border-[#4a5568] text-sm rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="bg-blue-600  text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-[#a0aec0] mt-2 hidden">
          {'Examples: "Add a task to buy groceries", "Show me my tasks", "Complete the meeting task"'}
        </p>
      </form>
    </div>
  );
};

export default ChatInterface;