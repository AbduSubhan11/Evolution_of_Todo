interface ChatRequest {
  conversation_id?: string;
  message: string;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: Array<any>;
  status: string;
}

/**
 * Send a message to the AI chatbot API
 */
export const sendMessage = async (
  message: string,
  userId: string,
  token: string, // Add token as a parameter
  conversationId?: string
): Promise<ChatResponse> => {
  try {
    const requestBody: ChatRequest = {
      message,
    };

    if (conversationId) {
      requestBody.conversation_id = conversationId;
    }

    // Construct the API endpoint - it should match the backend endpoint
    // Point to backend server running on port 8000
    const response = await fetch(`http://localhost:8000/api/v1/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, // Include the token in the header
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data: ChatResponse = await response.json();

    // Trigger a refresh of the task list if the message contains task operations
    if (containsTaskOperation(message)) {
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('taskListRefresh'));
      }, 1000); // Delay to allow the backend to process the operation
    }

    return data;
  } catch (error) {
    console.error('Error sending message to chat API:', error);
    throw error;
  }
};

/**
 * Check if the message contains task operation keywords
 */
const containsTaskOperation = (message: string): boolean => {
  const taskKeywords = [
    'add', 'create', 'new', 'task',
    'update', 'change', 'modify', 'edit',
    'complete', 'done', 'finish', 'mark as done',
    'uncomplete', 'reopen', 'reset', 'mark as pending',
    'delete', 'remove', 'erase', 'cancel'
  ];

  const lowerMessage = message.toLowerCase();
  return taskKeywords.some(keyword => lowerMessage.includes(keyword));
};

/**
 * Create a new conversation
 */
export const createConversation = async (userId: string, token: string): Promise<string> => {
  // For now, we'll just return a placeholder
  // In a real implementation, this would call an API to create a conversation
  return `conv_${Date.now()}`;
};

/**
 * Get conversation history
 */
export const getConversationHistory = async (
  userId: string,
  conversationId: string,
  token: string
): Promise<any[]> => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/${userId}/chat/${conversationId}/history`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch conversation history');
    }

    const data = await response.json();
    return data.messages || [];
  } catch (error) {
    console.error('Error fetching conversation history:', error);
    return []; // Return empty array on error
  }
};