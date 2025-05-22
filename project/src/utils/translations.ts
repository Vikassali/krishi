import { Language, TranslationKey } from '../types';

export const translations: Record<Language, Record<TranslationKey, string>> = {
  english: {
    welcome: 'Hello! I am your agricultural assistant. Ask me about crop prices or any farming related questions.',
    listening: 'Listening...',
    cropPriceIntro: 'Here are the current crop prices:',
    askMeAboutCrops: 'You can ask me about crop prices by saying something like "What is the price of rice today?"',
    defaultResponse: 'I didn\'t understand that. Could you please ask about crop prices or farming information?',
    errorMessage: 'Sorry, I couldn\'t process your voice input. Please try again or type your question.'
  },
  kannada: {
    welcome: 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಕೃಷಿ ಸಹಾಯಕ. ಬೆಳೆ ಬೆಲೆಗಳ ಬಗ್ಗೆ ಅಥವಾ ಯಾವುದೇ ಕೃಷಿ ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳನ್ನು ನನ್ನನ್ನು ಕೇಳಿ.',
    listening: 'ಆಲಿಸುತ್ತಿದ್ದೇನೆ...',
    cropPriceIntro: 'ಇಲ್ಲಿ ಪ್ರಸ್ತುತ ಬೆಳೆ ಬೆಲೆಗಳಿವೆ:',
    askMeAboutCrops: 'ನೀವು "ಇಂದು ಅಕ್ಕಿಯ ಬೆಲೆ ಎಷ್ಟು?" ಎಂದು ಹೇಳುವ ಮೂಲಕ ಬೆಳೆ ಬೆಲೆಗಳ ಬಗ್ಗೆ ನನ್ನನ್ನು ಕೇಳಬಹುದು.',
    defaultResponse: 'ನನಗೆ ಅದು ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಬೆಳೆ ಬೆಲೆಗಳ ಬಗ್ಗೆ ಅಥವಾ ಕೃಷಿ ಮಾಹಿತಿಯನ್ನು ಕೇಳಬಹುದೇ?',
    errorMessage: 'ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಧ್ವನಿ ಇನ್‌ಪುಟ್ ಅನ್ನು ಸಂಸ್ಕರಿಸಲು ನನಗೆ ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ.'
  },
  hindi: {
    welcome: 'नमस्ते! मैं आपका कृषि सहायक हूं। मुझसे फसल की कीमतों या किसी भी खेती से संबंधित प्रश्न पूछें।',
    listening: 'सुन रहा हूं...',
    cropPriceIntro: 'यहां वर्तमान फसल कीमतें हैं:',
    askMeAboutCrops: 'आप "आज चावल का भाव क्या है?" जैसा कुछ कहकर फसल की कीमतों के बारे में मुझसे पूछ सकते हैं।',
    defaultResponse: 'मुझे वह समझ में नहीं आया। कृपया फसल की कीमतों या खेती की जानकारी के बारे में पूछें।',
    errorMessage: 'क्षमा करें, मैं आपके आवाज इनपुट को प्रोसेस नहीं कर सका। कृपया फिर से प्रयास करें या अपना प्रश्न टाइप करें।'
  }
};