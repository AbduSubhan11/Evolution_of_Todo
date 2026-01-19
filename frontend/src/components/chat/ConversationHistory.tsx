import React, { useState, useEffect } from 'react';

interface Conversation {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
}

interface ConversationHistoryProps {
  onSelectConversation: (conversationId: string) => void;
  currentConversationId?: string;
}

const ConversationHistory: React.FC<ConversationHistoryProps> = ({
  onSelectConversation,
  currentConversationId
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real implementation, this would fetch conversation history from the backend
    // For now, we'll simulate with mock data
    const mockConversations: Conversation[] = [
      {
        id: 'conv-1',
        title: 'Task Management',
        lastMessage: 'Added grocery list',
        timestamp: new Date(Date.now() - 3600000), // 1 hour ago
      },
      {
        id: 'conv-2',
        title: 'Project Updates',
        lastMessage: 'Updated project timeline',
        timestamp: new Date(Date.now() - 86400000), // 1 day ago
      },
      {
        id: 'conv-3',
        title: 'Weekly Planning',
        lastMessage: 'Completed weekly tasks',
        timestamp: new Date(Date.now() - 172800000), // 2 days ago
      },
    ];

    setConversations(mockConversations);
    setLoading(false);
  }, []);

  const handleSelectConversation = (id: string) => {
    onSelectConversation(id);
  };

  const formatDate = (date: Date) => {
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  if (loading) {
    return (
      <div className="p-4">
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-12 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="border-r border-gray-200 w-64 flex-shrink-0 hidden md:block">
      <div className="p-4 border-b">
        <h3 className="font-semibold text-lg">Conversations</h3>
      </div>
      <div className="overflow-y-auto max-h-[calc(100vh-200px)]">
        {conversations.length > 0 ? (
          <ul>
            {conversations.map((conversation) => (
              <li key={conversation.id}>
                <button
                  onClick={() => handleSelectConversation(conversation.id)}
                  className={`w-full text-left p-4 border-b hover:bg-gray-50 transition-colors ${
                    currentConversationId === conversation.id
                      ? 'bg-blue-50 border-l-4 border-l-blue-500'
                      : ''
                  }`}
                >
                  <div className="font-medium truncate">{conversation.title}</div>
                  <div className="text-sm text-gray-600 truncate">{conversation.lastMessage}</div>
                  <div className="text-xs text-gray-400 mt-1">
                    {formatDate(conversation.timestamp)}
                  </div>
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <div className="p-4 text-center text-gray-500">
            No conversations yet
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationHistory;