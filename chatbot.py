from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Dental clinic price list (used in chatbot responses)
price_list = """
🦷 DENTAL CLINIC PRICE LIST

🔹 STANDARD PROCEDURES:
- Dental Consultation: ₱500
- Oral Prophylaxis (Cleaning): ₱800
- Permanent Filling (Light Cure): ₱800 + ₱200/surface
- Simple Extraction: ₱800

🔹 SPECIAL CASES:
- Deep Cleaning: ₱1,500 – ₱2,500
- Difficult Extraction: ₱1,500 – ₱2,500
- Additional Carpule/Syringe: ₱200 each

🔹 PROSTHESIS:
- Unilateral Acrylic Denture: starts ₱5,000 + ₱500/tooth
- Bilateral Acrylic Denture: starts ₱7,500 + ₱500/tooth
- Complete Denture (Acrylic Base): ₱30,000 (₱15,000 upper + ₱15,000 lower)

🔹 FLEXIBLE DENTURES:
- Unilateral: ₱10,000 + ₱500/tooth
- Bilateral: ₱15,000 + ₱500/tooth
- Complete Upper & Lower: ₱40,000 (₱20,000 each)

🔹 METAL FRAMEWORK:
- Upper or Lower: starts ₱15,000 + ₱500/tooth
- Complete Set (Upper & Lower): ₱35,000

🔹 CROWNS & BRIDGES:
- Metal Porcelain Crown: ₱8,000/tooth
- Emax: ₱12,000/tooth
- Zirconia: ₱15,000/tooth

🔹 RETAINERS & OTHER DEVICES:
- Hawley Retainer: ₱6,000 (upper or lower)
- Clear Retainer: ₱8,000 (upper or lower)
- Mouth Guard: ₱10,000
- Inclined Plane: ₱8,000

🔹 ORTHODONTICS:
- Braces (Upper or Lower): ₱30,000
- Braces (Complete Set): starts ₱50,000 (case-dependent)

📞 Contact us for appointments or inquiries.
"""

def dental_ai_response(message):
    message = message.lower()
    
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    farewell = ["goodbye", "bye", "see you later", "take care", "bye for now"]
    
    if any(greet in message for greet in greetings):
        return random.choice([
            "Hello! How can I assist you with your dental needs today?",
            "Hi there! How can I help you with your dental concerns?",
            "Hey! Need help with something about your teeth?"
        ])
    
    elif any(fare in message for fare in farewell):
        return random.choice([
            "Goodbye! Take care of your smile!",
            "See you later! Stay healthy!",
            "Take care! Don't forget to brush your teeth!"
        ])
    
    elif "price list" in message or "services" in message or "price" in message or "fee" in message:
        return price_list

    elif "consultation" in message:
        return "A standard dental consultation is ₱500."

    elif "oral prophylaxis" in message or "cleaning" in message:
        return "Oral Prophylaxis (teeth cleaning) costs ₱800. Deep cleaning ranges from ₱1,500 to ₱2,500."

    elif "filling" in message or "light cure" in message:
        return "A light cure permanent filling costs ₱800. Additional ₱200 per surface if needed."

    elif "extraction" in message:
        return "A simple tooth extraction costs ₱800. Difficult extractions range from ₱1,500 to ₱2,500."

    elif "carpule" in message or "syringe" in message:
        return "An additional carpule or syringe costs ₱200 each."

    elif "unilateral acrylic" in message:
        return "Unilateral acrylic base dentures start at ₱5,000 plus ₱500 per tooth."

    elif "bilateral acrylic" in message:
        return "Bilateral acrylic base dentures start at ₱7,500 plus ₱500 per tooth."

    elif "complete denture acrylic" in message:
        return "Complete denture acrylic base costs ₱30,000 (₱15,000 upper and ₱15,000 lower)."

    elif "flexible denture" in message:
        return "Flexible dentures: Unilateral ₱10,000 + ₱500/tooth; Bilateral ₱15,000 + ₱500/tooth; Complete ₱40,000 (₱20,000 each)."

    elif "metal framework" in message:
        return "Metal framework dentures start at ₱15,000 (upper or lower), plus ₱500 per tooth. Complete set is ₱35,000."

    elif "crown" in message or "bridges" in message:
        return (
            "Crowns and Bridges:\n"
            "- Metal porcelain crown: ₱8,000 per tooth\n"
            "- Emax: ₱12,000 per tooth\n"
            "- Zirconia: ₱15,000 per tooth"
        )

    elif "hawley" in message:
        return "Hawley retainers cost ₱6,000 (upper or lower)."

    elif "clear retainer" in message:
        return "Clear retainers cost ₱8,000 (upper or lower)."

    elif "mouth guard" in message:
        return "A custom mouth guard costs ₱10,000."

    elif "inclined plane" in message:
        return "Inclined plane therapy appliance costs ₱8,000."

    elif "braces" in message:
        return (
            "Braces pricing:\n"
            "- Upper or Lower only: ₱30,000\n"
            "- Both (Up and Down): Starts at ₱50,000 (case-based)"
        )

    elif "appointment" in message:
        return "You can book an appointment by visiting our website or calling our clinic. We'd be happy to assist you!"

    elif "toothache" in message:
        return "For a toothache, rinse with warm salt water and consult your dentist as soon as possible."

    else:
        return "I'm here to help with dental questions. Please ask about a procedure, price, or appointment."

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    reply = dental_ai_response(user_input)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
