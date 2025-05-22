from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# --- Load your trained ML model ---
MODEL_PATH = 'crop_price_model.pkl'
model = joblib.load(MODEL_PATH)

# 1. Vegetable Prices Data (English, Kannada, Hindi)
VEGETABLE_PRICES = {
    "tomato": 35, "potato": 28, "onion": 40, "carrot": 50, "rice": 60, "wheat": 55, "maize": 45,
    "cabbage": 30, "cauliflower": 38, "spinach": 25, "cucumber": 22, "bell pepper": 70, "green peas": 80,
    "beans": 60, "eggplant": 45, "garlic": 120, "ginger": 110, "chili": 150, "pumpkin": 20, "sweet potato": 40,
    "radish": 18, "lettuce": 35, "corn": 50, "bitter gourd": 55, "okra": 48, "brinjal": 42, "mustard greens": 30,
    "fenugreek": 28, "coriander": 25, "mint": 22, "lemon": 60, "banana": 45, "apple": 120, "orange": 80,
    "grapes": 150, "mango": 100, "pomegranate": 130, "watermelon": 25, "papaya": 30, "pineapple": 50,
    "guava": 40, "pear": 90, "cherry": 200, "strawberry": 250, "blackberry": 220, "blueberry": 300,
    "coconut": 60, "cashew nut": 900, "almond": 800, "walnut": 750, "peanut": 100, "sesame": 120,
    "sunflower seed": 110, "soybean": 70, "lentil": 90, "chickpea": 85, "kidney bean": 95, "black gram": 80,
    "green gram": 75, "mustard seed": 100, "sugarcane": 40, "tea leaves": 500, "coffee beans": 600,
    "cotton": 120, "jute": 50, "tobacco": 150, "turmeric": 250, "cumin": 300, "cardamom": 1500, "clove": 1200,
    "black pepper": 1400, "vanilla": 2500, "basil": 40, "oregano": 45, "thyme": 50, "rosemary": 55, "sage": 60,
    "asparagus": 150, "artichoke": 200, "arugula": 70, "beetroot": 30, "bok choy": 35, "broccoli": 60,
    "brussels sprouts": 80, "kale": 50, "collard greens": 45, "endive": 55, "fennel": 40, "kohlrabi": 35,
    "leek": 45, "parsnip": 50, "rutabaga": 40, "shallot": 90, "swiss chard": 50, "turnip": 30, "zucchini": 40,
    "yam": 60, "cassava": 45, "jicama": 55, "water chestnut": 65, "lotus root": 70, "edamame": 80,
    "chayote": 35, "celery": 30, "celtuce": 40, "daikon": 25, "dandelion greens": 30, "horseradish": 90,
    "wasabi": 1500
}

# 2. Crop Name Translations (English <-> Kannada <-> Hindi)
CROP_TRANSLATIONS = {
    "kannada": {
        "ಟೊಮೇಟೊ": "tomato", "ಆಲೂಗಡ್ಡೆ": "potato", "ಈರುಳ್ಳಿ": "onion", "ಕ್ಯಾರೆಟ್": "carrot",
        "ಅಕ್ಕಿ": "rice", "ಗೋಧಿ": "wheat", "ಮಕ್ಕಜೋಳ": "maize", "ಹುಲ್ಲು": "spinach",
        "ಸೌತೆಕಾಯಿ": "cucumber", "ಬೆಲ್ ಪೆಪ್ಪರ್": "bell pepper", "ಹಸಿರು ಬಟಾಣಿ": "green peas",
        "ಹುರುಳಿಕಾಯಿ": "beans", "ಬದನೆಕಾಯಿ": "eggplant", "ಬೆಳ್ಳುಳ್ಳಿ": "garlic", "ಶುಂಠಿ": "ginger",
        "ಮೆಣಸು": "chili", "ಕುಂಬಳಕಾಯಿ": "pumpkin", "ಸಿಹಿ ಆಲೂಗಡ್ಡೆ": "sweet potato",
        "ಮೂಲಂಗಿ": "radish", "ಹುಳಿವಳ್ಳಿ": "lettuce", "ಜೋಳ": "corn", "ಹಾಗಲಕಾಯಿ": "bitter gourd",
        "ಬೆಂಡೆಕಾಯಿ": "okra", "ಬ್ರಿಂಜಲ್": "brinjal", "ಸಾಸಿವೆ ಸೊಪ್ಪು": "mustard greens",
        "ಮೆಂತ್ಯೆ": "fenugreek", "ಕೊತ್ತಂಬರಿ": "coriander", "ಪುದೀನಾ": "mint", "ನಿಂಬೆ": "lemon",
        "ಬಾಳೆಹಣ್ಣು": "banana", "ಸೇಬು": "apple", "ಕಿತ್ತಳೆ": "orange", "ದ್ರಾಕ್ಷಿ": "grapes",
        "ಮಾವು": "mango", "ದಾಳಿಂಬೆ": "pomegranate", "ಕಲ್ಲಂಗಡಿ": "watermelon", "ಪಪಾಯಿ": "papaya",
        "ಅನಾನಸ್": "pineapple", "ಪೇರಲೆ": "guava", "ನಾಶ್ಪತಿ": "pear", "ಚೆರ್ರಿ": "cherry",
        "ಸ್ಟ್ರಾಬೆರಿ": "strawberry", "ಬ್ಲ್ಯಾಕ್ಬೆರಿ": "blackberry", "ನೀಲಿ ಹಣ್ಣು": "blueberry",
        "ತೆಂಗಿನಕಾಯಿ": "coconut", "ಗೋಡಂಬಿ": "cashew nut", "ಬಾದಾಮಿ": "almond", "ಅಕ್ರೋಟ್": "walnut",
        "ಶೆಂಗಾ": "peanut", "ಎಳ್ಳು": "sesame", "ಸೂರ್ಯಕಾಂತಿ ಬೀಜ": "sunflower seed",
        "ಸೊಯಾಬೀನ್": "soybean", "ಹುರಳಿಕಾಳು": "lentil", "ಕಡಲೆ": "chickpea", "ಅಲಸು": "kidney bean",
        "ಉದ್ದಿನಕಾಳು": "black gram", "ಹೆಸರುಕಾಳು": "green gram", "ಸಾಸಿವೆ": "mustard seed",
        "ಶುಗರಕೇನ್": "sugarcane", "ಚಹಾ ಎಲೆ": "tea leaves", "ಕಾಫಿ ಬೀಜ": "coffee beans",
        "ಹತ್ತಿ": "cotton", "ಜ್ಯೂಟ್": "jute", "ಧೂಮಪಾನ": "tobacco", "ಅರಿಶಿಣ": "turmeric",
        "ಜೀರಿಗೆ": "cumin", "ಏಲಕ್ಕಿ": "cardamom", "ಲವಂಗ": "clove", "ಮೆಣಸು": "black pepper",
        "ವ್ಯಾನಿಲ್ಲಾ": "vanilla", "ತಳಸೊಪ್ಪು": "basil", "ಓರೆಗಾನೋ": "oregano", "ಥೈಮ್": "thyme",
        "ರೋಸ್ಮೆರೀ": "rosemary", "ಸೇಜ್": "sage", "ಅಸ್ಪಾರಾಗಸ್": "asparagus", "ಆರ್ಟಿಚೋಕ್": "artichoke",
        "ಅರುಗುಲಾ": "arugula", "ಬೀಟ್ರೂಟ್": "beetroot", "ಬೋಕ್ ಚೋಯ್": "bok choy", "ಬ್ರೋಕೊಲಿ": "broccoli",
        "ಬ್ರಸೆಲ್ಸ್ ಸ್ಪ್ರೌಟ್ಸ್": "brussels sprouts", "ಕೇಲ್": "kale", "ಕಾಲರ್ಡ್ ಗ್ರೀನ್ಸ್": "collard greens",
        "ಎಂಡೈವ್": "endive", "ಸೋಂಪು": "fennel", "ಕೊಲ್ರಾಬಿ": "kohlrabi", "ಲೀಕ್": "leek",
        "ಪಾರ್ಸ್ನಿಪ್": "parsnip", "ರೂಟಬಾಗಾ": "rutabaga", "ಶಲ್ಲೋಟ್": "shallot",
        "ಸ್ವಿಸ್ ಚಾರ್ಡ್": "swiss chard", "ಟರ್ನಿಪ್": "turnip", "ಜುಕ್ಕಿನಿ": "zucchini", "ರತ್ತಾಳು": "yam",
        "ಮರಗೆಣಸು": "cassava", "ಜಿಕಾಮಾ": "jicama", "ನೀರು ಅಲಸು": "water chestnut",
        "ತಾಮರ ಹಣ್ಣು": "lotus root", "ಎಡಾಮಾಮೆ": "edamame", "ಚಯೋಟೆ": "chayote", "ಸೆಲರಿ": "celery",
        "ಸೆಲ್ಟ್ಯೂಸ್": "celtuce", "ಡೈಕಾನ್": "daikon", "ಡಾಂಡಲಿಯನ್ ಸೊಪ್ಪು": "dandelion greens",
        "ಹಾರ್ಸ್ರಾಡಿಷ್": "horseradish", "ವಸಾಬಿ": "wasabi"
    },
    "hindi": {
        "टमाटर": "tomato", "आलू": "potato", "प्याज": "onion", "गाजर": "carrot",
        "चावल": "rice", "गेहूं": "wheat", "मक्का": "maize", "पालक": "spinach",
        "खीरा": "cucumber", "शिमला मिर्च": "bell pepper", "हरी मटर": "green peas",
        "फली": "beans", "बैंगन": "eggplant", "लहसुन": "garlic", "अदरक": "ginger",
        "मिर्च": "chili", "कद्दू": "pumpkin", "शकरकंद": "sweet potato", "मूली": "radish",
        "सलाद": "lettuce", "मक्का": "corn", "करेला": "bitter gourd", "भिंडी": "okra",
        "बैंगन": "brinjal", "सरसों": "mustard greens", "मेथी": "fenugreek", "धनिया": "coriander",
        "पुदीना": "mint", "नींबू": "lemon", "केला": "banana", "सेब": "apple", "संतरा": "orange",
        "अंगूर": "grapes", "आम": "mango", "अनार": "pomegranate", "तरबूज": "watermelon",
        "पपीता": "papaya", "अनानास": "pineapple", "अमरूद": "guava", "नाशपाती": "pear",
        "चेरी": "cherry", "स्ट्रॉबेरी": "strawberry", "ब्लैकबेरी": "blackberry", "ब्लूबेरी": "blueberry",
        "नारियल": "coconut", "काजू": "cashew nut", "बादाम": "almond", "अखरोट": "walnut",
        "मूंगफली": "peanut", "तिल": "sesame", "सूरजमुखी बीज": "sunflower seed", "सोयाबीन": "soybean",
        "मसूर": "lentil", "चना": "chickpea", "राजमा": "kidney bean", "उड़द": "black gram",
        "मूंग": "green gram", "सरसों": "mustard seed", "गन्ना": "sugarcane", "चाय पत्ती": "tea leaves",
        "कॉफी बीन्स": "coffee beans", "कपास": "cotton", "जूट": "jute", "तंबाकू": "tobacco",
        "हल्दी": "turmeric", "जीरा": "cumin", "इलायची": "cardamom", "लौंग": "clove",
        "काली मिर्च": "black pepper", "वनीला": "vanilla", "तुलसी": "basil", "ओरिगैनो": "oregano",
        "थाइम": "thyme", "रोसमेरी": "rosemary", "सेज": "sage", "एस्पैरेगस": "asparagus",
        "आर्टिचोक": "artichoke", "अरुगुला": "arugula", "चुकंदर": "beetroot", "बोक चॉय": "bok choy",
        "ब्रोकोली": "broccoli", "ब्रसेल्स स्प्राउट्स": "brussels sprouts", "केल": "kale",
        "कोलार्ड ग्रीन्स": "collard greens", "एंडिव": "endive", "सौंफ": "fennel",
        "कोलरबी": "kohlrabi", "लीक": "leek", "पार्सनिप": "parsnip", "रutabaga": "rutabaga",
        "शलगम": "turnip", "जुकिनी": "zucchini", "शकरकंद": "yam", "कसावा": "cassava",
        "जिकामा": "jicama", "पानीफल": "water chestnut", "कमल ककड़ी": "lotus root",
        "एडामामे": "edamame", "चायोटे": "chayote", "अजवाइन": "celery", "सेल्ट्यूस": "celtuce",
        "डाइकॉन": "daikon", "डंडेलियन ग्रीन्स": "dandelion greens", "हॉर्सरैडिश": "horseradish",
        "वसाबी": "wasabi"
    }
}

# 3. Price Query Logic
def get_price_reply(user_message, language):
    msg = user_message.lower()
    price_patterns = [
        r"\bprice\b", r"\brate\b", r"\bcost\b", r"\bmarket price\b",
        r"\bಬೆಲೆ\b", r"\bದರ\b", r"\bಮಾರುಕಟ್ಟೆ ಬೆಲೆ\b",
        r"\bकीमत\b", r"\bभाव\b", r"\bमूल्य\b", r"\bबाज़ार भाव\b"
    ]
    price_regex = "|".join(price_patterns)
    if re.search(price_regex, msg):
        # 1. Try English crop names
        for item in VEGETABLE_PRICES:
            if re.search(rf"\b{item}\b", msg):
                price = VEGETABLE_PRICES[item]
                if language == "kannada":
                    return f"{item.capitalize()} ನ ಬೆಲೆ ಪ್ರತಿ ಕೆಜಿಗೆ ₹{price} ಆಗಿದೆ."
                elif language == "hindi":
                    return f"{item.capitalize()} की कीमत ₹{price} प्रति किलो है।"
                else:
                    return f"The current price of {item} is ₹{price} per kg."
        # 2. Try local language crop names
        if language in CROP_TRANSLATIONS:
            for local_name, eng_name in CROP_TRANSLATIONS[language].items():
                if re.search(local_name, msg):
                    price = VEGETABLE_PRICES.get(eng_name)
                    if price:
                        if language == "kannada":
                            return f"{local_name} ({eng_name}) ನ ಬೆಲೆ ಪ್ರತಿ ಕೆಜಿಗೆ ₹{price} ಆಗಿದೆ."
                        elif language == "hindi":
                            return f"{local_name} ({eng_name}) की कीमत ₹{price} प्रति किलो है।"
        # 3. Fallback
        return {
            "english": "Please specify the crop or vegetable you want the price for.",
            "kannada": "ದಯವಿಟ್ಟು ನೀವು ಬೆಲೆಯನ್ನು ತಿಳಿಯಲು ಬಯಸುವ ಬೆಳೆ ಅಥವಾ ತರಕಾರಿಯನ್ನು ನಮೂದಿಸಿ.",
            "hindi": "कृपया उस फसल या सब्जी का नाम बताएं जिसकी कीमत आप जानना चाहते हैं।"
        }.get(language, "Please specify the crop or vegetable you want the price for.")
    return None

# 4. Basic Questions and Small Talk Patterns
BASIC_PATTERNS_RESPONSES = [
    (r"\bhow are you\b|\bhow do you do\b", {
        "english": "I'm just a bot, but I'm doing great! How can I help you today?",
        "hindi": "मैं एक बॉट हूँ, लेकिन मैं ठीक हूँ! मैं आपकी कैसे मदद कर सकता हूँ?",
        "kannada": "ನಾನು ಬಾಟ್ ಆಗಿದ್ದೇನೆ, ಆದರೆ ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ! ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
    }),
    (r"\bwhat('?s| is) your name\b", {
        "english": "I'm your Agri Assistant Bot.",
        "hindi": "मेरा नाम एग्री असिस्टेंट बॉट है।",
        "kannada": "ನನ್ನ ಹೆಸರು ಕೃಷಿ ಸಹಾಯಕರ ಬಾಟ್."
    }),
    (r"\bwho (created|made|developed) you\b", {
        "english": "I was created by a team of developers to help you with crop prices and information.",
        "hindi": "मुझे डेवलपर्स की एक टीम ने आपकी सहायता के लिए बनाया है।",
        "kannada": "ನನ್ನನ್ನು ಅಭಿವೃದ್ಧಿಪಡಿಸಿದವರು ಅಭಿವೃದ್ಧಿಕರ್ತರ ತಂಡ."
    }),
    (r"\bthank(s| you)\b|\bthanks a lot\b", {
        "english": "You're welcome! Let me know if you have more questions.",
        "hindi": "आपका स्वागत है! अगर आपके पास और सवाल हैं तो बताएं।",
        "kannada": "ನಿಮಗೆ ಧನ್ಯವಾದಗಳು! ನಿಮಗೆ ಇನ್ನಷ್ಟು ಪ್ರಶ್ನೆಗಳಿದ್ದರೆ ಕೇಳಿ."
    }),
    (r"\bgoodbye\b|\bbye\b|\bsee you\b", {
        "english": "Goodbye! Have a great day!",
        "hindi": "अलविदा! आपका दिन शुभ हो!",
        "kannada": "ವಿದಾಯ! ನಿಮ್ಮ ದಿನ ಶುಭವಾಗಿರಲಿ!"
    }),
    (r"\bwhat('?s| is) the weather\b|\bweather today\b", {
        "english": "I can't provide live weather updates yet, but I can help with crop prices.",
        "hindi": "मैं अभी मौसम की जानकारी नहीं दे सकता, लेकिन फसल के दाम बता सकता हूँ।",
        "kannada": "ನಾನು ಹವಾಮಾನ ಮಾಹಿತಿ ನೀಡಲು ಸಾಧ್ಯವಿಲ್ಲ, ಆದರೆ ಬೆಲೆ ಮಾಹಿತಿ ನೀಡಬಹುದು."
    }),
    (r"\bhelp\b|\bassistance\b|\bsupport\b", {
        "english": "Sure, I can help you. Please tell me your question.",
        "hindi": "ज़रूर, मैं आपकी सहायता कर सकता हूँ। कृपया अपना प्रश्न बताएं।",
        "kannada": "ಖಚಿತವಾಗಿ, ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಹೇಳಿ."
    }),
    (r"\bwho are you\b|\bwhat are you\b", {
        "english": "I'm your friendly Agri chatbot, here to help with crop prices and queries.",
        "hindi": "मैं आपका एग्री चैटबॉट हूँ, जो फसल के दाम और सवालों में मदद करता है।",
        "kannada": "ನಾನು ನಿಮ್ಮ ಕೃಷಿ ಚಾಟ್‌ಬಾಟ್, ಬೆಲೆ ಮತ್ತು ಪ್ರಶ್ನೆಗಳಿಗೆ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ."
    }),
    (r"\bwhat can you do\b|\byour features\b", {
        "english": "I can provide crop prices, answer basic questions, and assist you in English, Hindi, and Kannada.",
        "hindi": "मैं फसल के दाम, सामान्य सवालों के जवाब और हिंदी, अंग्रेज़ी, कन्नड़ में सहायता कर सकता हूँ।",
        "kannada": "ನಾನು ಬೆಲೆ ಮಾಹಿತಿ, ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರ, ಮತ್ತು ಕನ್ನಡ, ಇಂಗ್ಲಿಷ್, ಹಿಂದಿಯಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಹುದು."
    }),
    (r"\bare you a robot\b|\bare you human\b", {
        "english": "I'm a virtual assistant, not a human, but I'm here to help!",
        "hindi": "मैं एक वर्चुअल असिस्टेंट हूँ, इंसान नहीं, लेकिन आपकी मदद के लिए हूँ!",
        "kannada": "ನಾನು ವರ್ಚುವಲ್ ಸಹಾಯಕ, ಮಾನವ ಅಲ್ಲ, ಆದರೆ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ!"
    }),
    (r"\bhello\b|\bhi\b|\bhey\b", {
        "english": "Hello! How can I assist you today?",
        "hindi": "नमस्ते! मैं आपकी किस प्रकार सहायता कर सकता हूँ?",
        "kannada": "ಹಲೋ! ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
    }),
    # Add more patterns as needed!
]

def get_basic_reply(user_message, language):
    msg = user_message.lower()
    for pattern, responses in BASIC_PATTERNS_RESPONSES:
        if re.search(pattern, msg):
            return responses.get(language, responses["english"])
    return None

def get_default_reply(language):
    return {
        "english": "Sorry, I didn't understand that. Could you please rephrase?",
        "kannada": "ಕ್ಷಮಿಸಿ, ನಾನು ಅದನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.",
        "hindi": "माफ़ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा कहें।"
    }.get(language, "Sorry, I didn't understand that. Could you please rephrase?")

def get_bot_reply(user_message, language):
    price_reply = get_price_reply(user_message, language)
    if price_reply:
        return price_reply
    basic_reply = get_basic_reply(user_message, language)
    if basic_reply:
        return basic_reply
    return get_default_reply(language)

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.json
    user_message = data.get('message', '')
    language = data.get('language', 'english')
    response = {"reply": get_bot_reply(user_message, language)}
    return jsonify(response)

@app.route('/api/predict', methods=['POST'])
def predict_price():
    data = request.json
    try:
        features = []
        for col in ['crop', 'state', 'market', 'date']:
            features.append(data.get(col))
        features = np.array([features]).astype(float)
        prediction = model.predict(features)
        return jsonify({'predicted_price': float(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
