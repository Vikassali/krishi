import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Language, Message } from '../types';
import LanguageSelector from './LanguageSelector';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { translations } from '../utils/translations';
import { speak } from '../utils/speechRecognition';
import { Leaf } from 'lucide-react';

const ChatBot: React.FC = () => {
  const [language, setLanguage] = useState<Language>('english');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessage: Message = {
      id: 'welcome',
      text: translations[language].welcome,
      isBot: true,
      timestamp: new Date(),
      language: language
    };
    
    setMessages([welcomeMessage]);
    speak(welcomeMessage.text, language);
  }, [language]);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (isProcessing) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      isBot: false,
      timestamp: new Date(),
      language
    };
    setMessages(prev => [...prev, userMessage]);
    setIsProcessing(true);

    try {
      // Send message to Flask backend
      const res = await axios.post('http://localhost:5000/api/message', {
        message: text,
        language: language
      });

      const responseText = res.data.reply;

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: responseText,
        isBot: true,
        timestamp: new Date(),
        language
      };

      setMessages(prev => [...prev, botMessage]);
      // Speak the response
      speak(responseText, language);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        text: "Sorry, I couldn't reach the server.",
        isBot: true,
        timestamp: new Date(),
        language
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleLanguageChange = (newLanguage: Language) => {
    setLanguage(newLanguage);
  };

  return (
    <div className="flex flex-col h-full max-w-2xl mx-auto bg-gradient-to-b from-gray-50 to-gray-100 rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-white shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="bg-green-100 p-2 rounded-full">
            <Leaf size={20} className="text-green-600" />
          </div>
          <h1 className="text-xl font-semibold text-gray-800">AgriBot</h1>
        </div>
        <LanguageSelector 
          currentLanguage={language} 
          onLanguageChange={handleLanguageChange} 
        />
      </div>
      
      {/* Messages area */}
      <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
        <div className="space-y-2">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input area */}
      <div className="p-4 bg-gray-100 border-t border-gray-200">
        <ChatInput 
          onSendMessage={handleSendMessage} 
          language={language}
          disabled={isProcessing} 
        />
      </div>
    </div>
  );
};

export default ChatBot;