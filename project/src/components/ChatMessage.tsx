import React from 'react';
import { Message } from '../types';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const { text, isBot, timestamp } = message;
  
  // Format time from timestamp
  const formattedTime = new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(timestamp);

  return (
    <div 
      className={`flex gap-3 ${
        isBot ? 'justify-start' : 'justify-end'
      } mb-4 animate-fadeIn`}
    >
      {isBot && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-green-100 flex items-center justify-center">
          <Bot size={16} className="text-green-600" />
        </div>
      )}
      
      <div className={`relative max-w-[80%] px-4 py-2 rounded-lg ${
        isBot 
          ? 'bg-white text-gray-800 shadow-sm' 
          : 'bg-indigo-600 text-white'
      }`}>
        <div className="whitespace-pre-line text-sm">
          {text}
        </div>
        <span className={`block text-xs mt-1 ${
          isBot ? 'text-gray-500' : 'text-indigo-100'
        }`}>
          {formattedTime}
        </span>
      </div>
      
      {!isBot && (
        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center">
          <User size={16} className="text-indigo-600" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;