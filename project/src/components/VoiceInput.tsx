import React, { useState, useEffect } from 'react';
import { Mic, MicOff } from 'lucide-react';
import { Language } from '../types';
import { isSpeechRecognitionSupported, setupSpeechRecognition } from '../utils/speechRecognition';
import { translations } from '../utils/translations';

interface VoiceInputProps {
  language: Language;
  onSpeechResult: (text: string) => void;
  disabled?: boolean;
}

const VoiceInput: React.FC<VoiceInputProps> = ({ 
  language, 
  onSpeechResult, 
  disabled = false 
}) => {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const [ripples, setRipples] = useState<number[]>([]);

  useEffect(() => {
    setIsSupported(isSpeechRecognitionSupported());
  }, []);

  useEffect(() => {
    if (isListening) {
      const interval = setInterval(() => {
        setRipples(prev => [...prev, Date.now()]);
      }, 1000);
      
      return () => clearInterval(interval);
    }
  }, [isListening]);

  // Clean up old ripples
  useEffect(() => {
    if (ripples.length > 0) {
      const timeout = setTimeout(() => {
        setRipples(prev => prev.slice(1));
      }, 2000);
      
      return () => clearTimeout(timeout);
    }
  }, [ripples]);

  const toggleListening = () => {
    if (disabled || !isSupported) return;
    
    if (!isListening) {
      setIsListening(true);
      const stopListening = setupSpeechRecognition(
        language,
        (text) => {
          onSpeechResult(text);
          setIsListening(false);
        },
        () => setIsListening(true),
        () => setIsListening(false),
        (error) => {
          console.error('Speech recognition error:', error);
          setIsListening(false);
        }
      );
      
      // Stop listening after 10 seconds if no result
      setTimeout(() => {
        if (isListening) {
          stopListening();
          setIsListening(false);
        }
      }, 10000);
    } else {
      setIsListening(false);
    }
  };

  return (
    <div className="relative">
      <button
        onClick={toggleListening}
        disabled={disabled || !isSupported}
        className={`flex items-center justify-center w-12 h-12 rounded-full transition-all duration-300 ${
          isListening
            ? 'bg-red-500 text-white shadow-lg'
            : isSupported
            ? 'bg-indigo-600 text-white hover:bg-indigo-700'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
        aria-label={isListening ? 'Stop listening' : 'Start voice input'}
      >
        {isListening ? (
          <Mic size={20} className="animate-pulse" />
        ) : (
          <MicOff size={20} className={!isSupported ? 'opacity-50' : ''} />
        )}
        
        {/* Ripple effects */}
        {ripples.map((id) => (
          <span
            key={id}
            className="absolute inset-0 rounded-full bg-red-400 opacity-70 animate-ping"
            style={{ animationDuration: '2s' }}
          />
        ))}
      </button>
      
      {isListening && (
        <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap bg-gray-800 text-white text-xs px-2 py-1 rounded">
          {translations[language].listening}
        </div>
      )}
    </div>
  );
};

export default VoiceInput;