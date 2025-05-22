import React from 'react';
import { Language } from '../types';
import { Globe } from 'lucide-react';

interface LanguageSelectorProps {
  currentLanguage: Language;
  onLanguageChange: (language: Language) => void;
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ 
  currentLanguage, 
  onLanguageChange 
}) => {
  const languages: { value: Language; label: string }[] = [
    { value: 'english', label: 'English' },
    { value: 'kannada', label: 'ಕನ್ನಡ' },
    { value: 'hindi', label: 'हिंदी' }
  ];

  return (
    <div className="flex items-center mb-4">
      <div className="flex items-center space-x-2 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 shadow-md">
        <Globe size={16} className="text-indigo-600" />
        <div className="flex space-x-1">
          {languages.map((lang) => (
            <button
              key={lang.value}
              onClick={() => onLanguageChange(lang.value)}
              className={`px-3 py-1 text-sm rounded-full transition-all duration-200 ${
                currentLanguage === lang.value
                  ? 'bg-indigo-600 text-white font-medium shadow-sm'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {lang.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LanguageSelector;