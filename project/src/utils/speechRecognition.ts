import { Language } from '../types';

// Language codes for Web Speech API
const languageCodes: Record<Language, string> = {
  english: 'en-US',
  kannada: 'kn-IN',
  hindi: 'hi-IN'
};

// Check if browser supports speech recognition
export const isSpeechRecognitionSupported = (): boolean => {
  return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
};

// Speech recognition setup
export const setupSpeechRecognition = (
  language: Language,
  onResult: (text: string) => void,
  onStart: () => void,
  onEnd: () => void,
  onError: (error: any) => void
): (() => void) => {
  // If speech recognition is not supported
  if (!isSpeechRecognitionSupported()) {
    onError('Speech recognition not supported in this browser');
    return () => {};
  }

  // Initialize speech recognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  // Configure recognition
  recognition.lang = languageCodes[language];
  recognition.continuous = false;
  recognition.interimResults = false;

  // Set up event handlers
  recognition.onstart = onStart;
  recognition.onend = onEnd;
  recognition.onerror = onError;
  
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    onResult(transcript);
  };

  // Start recognition
  recognition.start();

  // Return function to stop recognition
  return () => {
    recognition.stop();
  };
};

// Text to speech setup
export const speak = (text: string, language: Language): void => {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = languageCodes[language];
    window.speechSynthesis.speak(utterance);
  }
};