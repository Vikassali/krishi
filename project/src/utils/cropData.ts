import { CropPrice } from '../types';

// Sample crop price data
export const cropPrices: Record<string, CropPrice[]> = {
  english: [
    { name: 'Rice', price: 1950, unit: 'per quintal' },
    { name: 'Wheat', price: 2015, unit: 'per quintal' },
    { name: 'Cotton', price: 6380, unit: 'per quintal' },
    { name: 'Sugarcane', price: 315, unit: 'per quintal' },
    { name: 'Corn', price: 1870, unit: 'per quintal' },
    { name: 'Soybean', price: 4300, unit: 'per quintal' },
    { name: 'Potato', price: 1400, unit: 'per quintal' },
    { name: 'Onion', price: 2200, unit: 'per quintal' },
    { name: 'Tomato', price: 1800, unit: 'per quintal' }
  ],
  kannada: [
    { name: 'ಅಕ್ಕಿ', price: 1950, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಗೋಧಿ', price: 2015, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಹತ್ತಿ', price: 6380, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಕಬ್ಬು', price: 315, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಮೆಕ್ಕೆಜೋಳ', price: 1870, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಸೋಯಾಬೀನ್', price: 4300, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಆಲೂಗಡ್ಡೆ', price: 1400, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಈರುಳ್ಳಿ', price: 2200, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' },
    { name: 'ಟೊಮೇಟೊ', price: 1800, unit: 'ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್' }
  ],
  hindi: [
    { name: 'चावल', price: 1950, unit: 'प्रति क्विंटल' },
    { name: 'गेहूं', price: 2015, unit: 'प्रति क्विंटल' },
    { name: 'कपास', price: 6380, unit: 'प्रति क्विंटल' },
    { name: 'गन्ना', price: 315, unit: 'प्रति क्विंटल' },
    { name: 'मक्का', price: 1870, unit: 'प्रति क्विंटल' },
    { name: 'सोयाबीन', price: 4300, unit: 'प्रति क्विंटल' },
    { name: 'आलू', price: 1400, unit: 'प्रति क्विंटल' },
    { name: 'प्याज', price: 2200, unit: 'प्रति क्विंटल' },
    { name: 'टमाटर', price: 1800, unit: 'प्रति क्विंटल' }
  ]
};

// Keywords for crop price detection in different languages
export const cropKeywords: Record<string, string[]> = {
  english: ['price', 'cost', 'rate', 'crop', 'market', 'today', 'current'],
  kannada: ['ಬೆಲೆ', 'ದರ', 'ಬೆಲೆ ಎಷ್ಟು', 'ಮಾರುಕಟ್ಟೆ', 'ಇಂದಿನ', 'ಪ್ರಸ್ತುತ'],
  hindi: ['दाम', 'कीमत', 'भाव', 'फसल', 'मंडी', 'आज', 'वर्तमान']
};