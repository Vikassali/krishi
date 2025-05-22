export type Language = 'english' | 'kannada' | 'hindi';

export interface Message {
  id: string;
  text: string;
  isBot: boolean;
  timestamp: Date;
  language: Language;
}

export interface CropPrice {
  name: string;
  price: number;
  unit: string;
}

export type TranslationKey = 
  | 'welcome'
  | 'listening'
  | 'cropPriceIntro'
  | 'askMeAboutCrops'
  | 'defaultResponse'
  | 'errorMessage';