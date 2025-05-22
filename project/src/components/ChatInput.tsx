import React, { useState } from 'react';
import { Send } from 'lucide-react';
import VoiceInput from './VoiceInput';
import { Language } from '../types';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  language: Language;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  language, 
  disabled = false 
}) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleVoiceInput = (text: string) => {
    if (text.trim()) {
      onSendMessage(text);
    }
  };

  const placeholders = {
    english: 'Type your message...',
    kannada: 'ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಟೈಪ್ ಮಾಡಿ...',
    hindi: 'अपना संदेश टाइप करें...'
  };

  return (
    <form 
      onSubmit={handleSubmit} 
      className="flex items-center gap-2 bg-white p-2 rounded-lg shadow-md border border-gray-200"
    >
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder={placeholders[language]}
        disabled={disabled}
        className="flex-1 py-2 px-3 bg-gray-50 rounded-md outline-none focus:ring-2 focus:ring-indigo-300 transition-all"
      />
      
      <VoiceInput 
        language={language} 
        onSpeechResult={handleVoiceInput}
        disabled={disabled} 
      />
      
      <button
        type="submit"
        disabled={!message.trim() || disabled}
        className={`flex items-center justify-center w-10 h-10 rounded-full transition-colors ${
          message.trim() && !disabled
            ? 'bg-indigo-600 text-white hover:bg-indigo-700'
            : 'bg-gray-200 text-gray-400 cursor-not-allowed'
        }`}
        aria-label="Send message"
      >
        <Send size={18} />
      </button>
    </form>
  );
};

export default ChatInput;