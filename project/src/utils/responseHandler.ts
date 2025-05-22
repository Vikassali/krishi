import { Language, CropPrice } from '../types';
import { cropPrices, cropKeywords } from './cropData';
import { translations } from './translations';

// Check if message is asking about crop prices
export const isAskingForCropPrices = (message: string, language: Language): boolean => {
  const keywords = cropKeywords[language];
  return keywords.some(keyword => message.toLowerCase().includes(keyword.toLowerCase()));
};

// Generate response for crop price inquiry
export const getCropPriceResponse = (message: string, language: Language): string => {
  const prices = cropPrices[language];
  
  // Check if asking for specific crop
  for (const crop of prices) {
    if (message.toLowerCase().includes(crop.name.toLowerCase())) {
      return `${crop.name}: ${crop.price} ${crop.unit}`;
    }
  }
  
  // If asking for all prices or no specific crop mentioned
  const intro = translations[language].cropPriceIntro;
  const priceList = prices.map(crop => `${crop.name}: ${crop.price} ${crop.unit}`).join('\n');
  
  return `${intro}\n${priceList}`;
};

// Get default response based on language
export const getDefaultResponse = (language: Language): string => {
  return translations[language].defaultResponse;
};

// Process user message and return appropriate response
export const processMessage = (message: string, language: Language): string => {
  if (isAskingForCropPrices(message, language)) {
    return getCropPriceResponse(message, language);
  }
  
  return getDefaultResponse(language);
};