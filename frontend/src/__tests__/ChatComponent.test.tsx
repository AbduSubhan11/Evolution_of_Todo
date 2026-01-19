import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { SessionProvider } from 'next-auth/react';
import ChatInterface from '../components/chat/ChatInterface';

// Mock the chat service
jest.mock('@/lib/chatService', () => ({
  sendMessage: jest.fn().mockResolvedValue({
    conversation_id: 'test-conversation-id',
    response: 'Test AI response',
    tool_calls: [],
    status: 'success'
  })
}));

// Mock the auth helper
jest.mock('@/lib/auth', () => ({
  getAccessToken: jest.fn().mockResolvedValue('test-token'),
  isAuthenticated: jest.fn().mockResolvedValue(true)
}));

describe('ChatInterface Component', () => {
  const mockSession = {
    expires: '1',
    user: { email: 'test@example.com', id: 'test-user-id' }
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders without crashing', () => {
    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    expect(screen.getByText('AI Todo Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your task management request...')).toBeInTheDocument();
  });

  it('displays initial welcome message', () => {
    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    expect(screen.getByText('Start a conversation to manage your tasks!')).toBeInTheDocument();
  });

  it('allows user to type and submit a message', async () => {
    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    const input = screen.getByPlaceholderText('Type your task management request...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Add a test task' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Add a test task')).toBeInTheDocument();
    });
  });

  it('displays AI response after sending a message', async () => {
    const mockSendMessage = require('@/lib/chatService').sendMessage as jest.MockedFunction<any>;

    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    const input = screen.getByPlaceholderText('Type your task management request...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith('Test message', 'test-user-id');
      expect(screen.getByText('Test AI response')).toBeInTheDocument();
    });
  });

  it('shows loading state when AI is responding', async () => {
    // Make the mock promise take longer to resolve
    jest.spyOn(require('@/lib/chatService'), 'sendMessage').mockImplementation(() => {
      return new Promise((resolve) => {
        setTimeout(() => resolve({
          conversation_id: 'test-conversation-id',
          response: 'Test AI response',
          tool_calls: [],
          status: 'success'
        }), 100);
      });
    });

    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    const input = screen.getByPlaceholderText('Type your task management request...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Check that loading indicator appears
    expect(screen.getByText(/Sending message.../)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Test AI response')).toBeInTheDocument();
    });
  });

  it('disables send button when input is empty', () => {
    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    const input = screen.getByPlaceholderText('Type your task management request...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    // Initially, input is empty, so button should be disabled
    expect(sendButton).toBeDisabled();

    fireEvent.change(input, { target: { value: 'Non-empty message' } });
    expect(sendButton).not.toBeDisabled();
  });

  it('displays error message when API call fails', async () => {
    // Mock an error response
    jest.spyOn(require('@/lib/chatService'), 'sendMessage').mockRejectedValue(new Error('API Error'));

    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    const input = screen.getByPlaceholderText('Type your task management request...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Sorry, I encountered an error processing your request.')).toBeInTheDocument();
    });
  });

  it('shows example prompts', () => {
    render(
      <SessionProvider session={mockSession}>
        <ChatInterface />
      </SessionProvider>
    );

    expect(screen.getByText('Examples:')).toBeInTheDocument();
    expect(screen.getByText('"Add a task to buy groceries"')).toBeInTheDocument();
  });
});