from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# 1. 100+ Crop Prices Data
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

# 2. Crop Name Translations (100+ for Kannada and Hindi, mapped to English)
CROP_TRANSLATIONS = {
    "kannada": {
        "ಟೊಮೇಟೊ": "tomato", "ಆಲೂಗಡ್ಡೆ": "potato", "ಈರುಳ್ಳಿ": "onion", "ಕ್ಯಾರೆಟ್": "carrot",
        "ಅಕ್ಕಿ": "rice", "ಗೋಧಿ": "wheat", "ಮೆಕ್ಕೆಜೋಳ": "maize", "ಎಲೆಕೋಸು": "cabbage", "ಹೂಕೋಸು": "cauliflower",
        "ಪಾಲಕ್": "spinach", "ಸೌತೆಕಾಯಿ": "cucumber", "ದೊಣ್ಣೆ ಮೆಣಸು": "bell pepper", "ಹಸಿರು ಬಟಾಣಿ": "green peas",
        "ಹುರಳಿಕಾಯಿ": "beans", "ಬದನೆಕಾಯಿ": "eggplant", "ಬೆಳ್ಳುಳ್ಳಿ": "garlic", "ಶುಂಠಿ": "ginger",
        "ಮೆಣಸು": "chili", "ಕುಂಬಳಕಾಯಿ": "pumpkin", "ಸಿಹಿ ಆಲೂಗಡ್ಡೆ": "sweet potato", "ಮೂಲಂಗಿ": "radish",
        "ಹೆಸರು": "lettuce", "ಜೋಳ": "corn", "ಹಾಗಲಕಾಯಿ": "bitter gourd", "ಬೆಂಡೆಕಾಯಿ": "okra",
        "ಬ್ರಿಂಜಲ್": "brinjal", "ಸಾಸಿವೆ ಸೊಪ್ಪು": "mustard greens", "ಮೆಂತ್ಯೆ": "fenugreek", "ಕೊತ್ತಂಬರಿ": "coriander",
        "ಪುದೀನಾ": "mint", "ನಿಂಬೆ": "lemon", "ಬಾಳೆಹಣ್ಣು": "banana", "ಸೇಬು": "apple", "ಕಿತ್ತಳೆ": "orange",
        "ದ್ರಾಕ್ಷಿ": "grapes", "ಮಾವು": "mango", "ದಾಳಿಂಬೆ": "pomegranate", "ಕಲ್ಲಂಗಡಿ": "watermelon",
        "ಪಪ್ಪಾಯಿ": "papaya", "ಅನಾನಸ್": "pineapple", "ಪೇರಲೆ": "guava", "ನಾಶ್ಪತಿ": "pear", "ಚೆರಿ": "cherry",
        "ಸ್ಟ್ರಾಬೆರಿ": "strawberry", "ಬ್ಲ್ಯಾಕ್ಬೆರಿ": "blackberry", "ಬ್ಲೂಬೆರಿ": "blueberry", "ತೆಂಗಿನಕಾಯಿ": "coconut",
        "ಗೋಡಂಬಿ": "cashew nut", "ಬಾದಾಮಿ": "almond", "ಅಕಹೋಡು": "walnut", "ಶೇಂಗಾ": "peanut", "ಎಳ್ಳು": "sesame",
        "ಸೂರ್ಯಕಾಂತಿ ಬೀಜ": "sunflower seed", "ಸೋಯಾಬೀನ್": "soybean", "ಹೆಸರುಕಾಳು": "lentil", "ಕಡಲೆ": "chickpea",
        "ರಾಜ್ಮಾ": "kidney bean", "ಉದ್ದಿನಕಾಳು": "black gram", "ಹೆಸರುಕಾಳು": "green gram", "ಸಾಸಿವೆ": "mustard seed",
        "ಶರಕರಿ": "sugarcane", "ಚಹಾ ಎಲೆ": "tea leaves", "ಕಾಫಿ ಬೀಜ": "coffee beans", "ಹತ್ತಿ": "cotton",
        "ಜ್ಯೂಟ್": "jute", "ಧೂಮಪಾನ": "tobacco", "ಅರಿಶಿನ": "turmeric", "ಜೀರಿಗೆ": "cumin", "ಏಲಕ್ಕಿ": "cardamom",
        "ಲವಂಗ": "clove", "ಕಪ್ಪು ಮೆಣಸು": "black pepper", "ವನಿಲ್ಲಾ": "vanilla", "ತುಳಸಿ": "basil", "ಓರೆಗಾನೋ": "oregano",
        "ತೈಮ್": "thyme", "ರೋಸ್‌ಮೇರಿ": "rosemary", "ಸೇಜ್": "sage", "ಅಸ್ಪಾರಾಗಸ್": "asparagus", "ಆರ್ಟಿಚೋಕ್": "artichoke",
        "ಅರುಗುಲಾ": "arugula", "ಬೀಟ್ರೂಟ್": "beetroot", "ಬೋಕ್ ಚೋಯ್": "bok choy", "ಬ್ರೊಕೊಲಿ": "broccoli",
        "ಬ್ರಸ್ಸೆಲ್ಸ್ ಸ್ಪ್ರೌಟ್": "brussels sprouts", "ಕೇಲ್": "kale", "ಕಾಲರ್ಡ್ ಗ್ರೀನ್ಸ್": "collard greens",
        "ಎಂಡೈವ್": "endive", "ಸೋಂಪು": "fennel", "ಕೋಲ್ರಾಬಿ": "kohlrabi", "ಲೀಕ್": "leek", "ಪಾರ್ಸ್ನಿಪ್": "parsnip",
        "ರೂಟಬಾಗಾ": "rutabaga", "ಶಲ್ಲೋಟ್": "shallot", "ಸ್ವಿಸ್ ಚಾರ್ಡ್": "swiss chard", "ಟರ್ನಿಪ್": "turnip",
        "ಜುಕ್ಕಿನಿ": "zucchini", "ರಾಟು": "yam", "ಕಸ್ಸಾವಾ": "cassava", "ಜಿಕಾಮಾ": "jicama", "ನೀರು ಕಸ್ತೂರಿ": "water chestnut",
        "ತಾವರೆ ಬೇರು": "lotus root", "ಎಡಮಾಮೆ": "edamame", "ಚಯೋಟೆ": "chayote", "ಸೆಲರಿ": "celery",
        "ಸೆಲ್ಟ್ಯೂಸ್": "celtuce", "ಡೈಕಾನ್": "daikon", "ದಾಂಡೇಲಿಯನ್ ಗ್ರೀನ್ಸ್": "dandelion greens",
        "ಹೋರ್ಸ್ರ್ಯಾಡಿಷ್": "horseradish", "ವಸಾಬಿ": "wasabi"
    },
    "hindi": {
        "टमाटर": "tomato", "आलू": "potato", "प्याज": "onion", "गाजर": "carrot", "चावल": "rice", "गेहूं": "wheat",
        "मक्का": "maize", "पत्ता गोभी": "cabbage", "फूलगोभी": "cauliflower", "पालक": "spinach", "खीरा": "cucumber",
        "शिमला मिर्च": "bell pepper", "मटर": "green peas", "फली": "beans", "बैंगन": "eggplant", "लहसुन": "garlic",
        "अदरक": "ginger", "मिर्च": "chili", "कद्दू": "pumpkin", "शकरकंद": "sweet potato", "मूली": "radish",
        "सलाद पत्ता": "lettuce", "मक्का": "corn", "करेला": "bitter gourd", "भिंडी": "okra", "ब्रिंजल": "brinjal",
        "सरसों का साग": "mustard greens", "मेथी": "fenugreek", "धनिया": "coriander", "पुदीना": "mint", "नींबू": "lemon",
        "केला": "banana", "सेब": "apple", "संतरा": "orange", "अंगूर": "grapes", "आम": "mango", "अनार": "pomegranate",
        "तरबूज": "watermelon", "पपीता": "papaya", "अनानास": "pineapple", "अमरूद": "guava", "नाशपाती": "pear",
        "चेरी": "cherry", "स्ट्रॉबेरी": "strawberry", "ब्लैकबेरी": "blackberry", "ब्लूबेरी": "blueberry",
        "नारियल": "coconut", "काजू": "cashew nut", "बादाम": "almond", "अखरोट": "walnut", "मूंगफली": "peanut",
        "तिल": "sesame", "सूरजमुखी बीज": "sunflower seed", "सोयाबीन": "soybean", "मसूर": "lentil", "चना": "chickpea",
        "राजमा": "kidney bean", "काला चना": "black gram", "हरा चना": "green gram", "सरसों": "mustard seed",
        "गन्ना": "sugarcane", "चाय पत्ती": "tea leaves", "कॉफी बीन्स": "coffee beans", "कपास": "cotton",
        "जूट": "jute", "तम्बाकू": "tobacco", "हल्दी": "turmeric", "जीरा": "cumin", "इलायची": "cardamom",
        "लौंग": "clove", "काली मिर्च": "black pepper", "वनीला": "vanilla", "तुलसी": "basil", "ओरिगैनो": "oregano",
        "थाइम": "thyme", "रोsemary": "rosemary", "सेज": "sage", "एस्पैरेगस": "asparagus", "आर्टिचोक": "artichoke",
        "अरुगुला": "arugula", "चुकंदर": "beetroot", "बोक चॉय": "bok choy", "ब्रोकली": "broccoli",
        "ब्रसेल्स स्प्राउट्स": "brussels sprouts", "केल": "kale", "कोलार्ड ग्रीन्स": "collard greens",
        "एंडिव": "endive", "सौंफ": "fennel", "कोहलाबी": "kohlrabi", "लीक": "leek", "पार्सनिप": "parsnip",
        "रutabaga": "rutabaga", "शलोट": "shallot", "स्विस चार्ड": "swiss chard", "शलजम": "turnip",
        "जुकिनी": "zucchini", "शकरकंद": "yam", "कसावा": "cassava", "जिकामा": "jicama", "सिंघाड़ा": "water chestnut",
        "कमल ककड़ी": "lotus root", "एडामेमे": "edamame", "चायोट": "chayote", "अजवाइन": "celery",
        "सेल्ट्यूज": "celtuce", "डाइकॉन": "daikon", "डंडेलियन ग्रीन्स": "dandelion greens",
        "हॉर्सरैडिश": "horseradish", "वसाबी": "wasabi"
    }
}

# 3. Price Query Logic
def get_price_reply(user_message, language):
    msg = user_message.lower()
    price_patterns = [
        r"\bprice\b", r"\brate\b", r"\bcost\b", r"\bmarket price\b",      # English
        r"\bಬೆಲೆ\b", r"\bದರ\b", r"\bಮಾರುಕಟ್ಟೆ ಬೆಲೆ\b",                      # Kannada
        r"\bकीमत\b", r"\bभाव\b", r"\bमूल्य\b", r"\bबाज़ार भाव\b"          # Hindi
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

# 4. Greetings and Help in All Languages
def get_greeting_reply(language):
    return {
        "english": "Hello! How can I assist you today?",
        "kannada": "ಹಲೋ! ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
        "hindi": "नमस्ते! मैं आपकी किस प्रकार सहायता कर सकता हूँ?"
    }.get(language, "Hello! How can I assist you today?")

def get_help_reply(language):
    return {
        "english": "Sure, I can help you. Please tell me your question.",
        "kannada": "ಖಚಿತವಾಗಿ, ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಹೇಳಿ.",
        "hindi": "ज़रूर, मैं आपकी सहायता कर सकता हूँ। कृपया अपना प्रश्न बताएं।"
    }.get(language, "Sure, I can help you. Please tell me your question.")

def get_default_reply(language):
    return {
        "english": "Sorry, I didn't understand that. Could you please rephrase?",
        "kannada": "ಕ್ಷಮಿಸಿ, ನಾನು ಅದನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.",
        "hindi": "माफ़ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा कहें।"
    }.get(language, "Sorry, I didn't understand that. Could you please rephrase?")

# 5. Main Bot Logic
def get_bot_reply(user_message, language):
    # 1. Price queries
    price_reply = get_price_reply(user_message, language)
    if price_reply:
        return price_reply
    # 2. Greetings
    if re.search(r'\bhello\b|\bhi\b|\bhey\b', user_message.lower()) or \
       (language == "kannada" and re.search(r'ಹಲೋ|ನಮಸ್ಕಾರ', user_message)) or \
       (language == "hindi" and re.search(r'नमस्ते|हैलो', user_message)):
        return get_greeting_reply(language)
    # 3. Help
    if re.search(r'\bhelp\b|\bassistance\b', user_message.lower()) or \
       (language == "kannada" and re.search(r'ಸಹಾಯ', user_message)) or \
       (language == "hindi" and re.search(r'मदद|सहायता', user_message)):
        return get_help_reply(language)
    # 4. Default fallback
    return get_default_reply(language)

# 6. Flask Endpoint
@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.json
    user_message = data.get('message', '')
    language = data.get('language', 'english')
    response = {"reply": get_bot_reply(user_message, language)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
