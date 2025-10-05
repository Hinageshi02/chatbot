from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import openai
import os

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")  # Or directly: "sk-..."

# ---------------------------
# Keyword-based logic (same as before)
# ---------------------------
# ... (Keep your dental_keywords and dental_ai_response logic here)

# ---------------------------
# GPT fallback for dental-only questions
# ---------------------------
def chatgpt_dental_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or gpt-3.5-turbo
            messages=[
                {"role": "system", 
                 "content": (
                    "You are a helpful assistant for a dental clinic. "
                    "Answer only questions related to dental treatments, procedures, prices, oral health, "
                    "or appointments. "
                    "If the question is unrelated to dentistry, politely respond: "
                    "'I'm sorry, I can only answer dental-related questions.'"
                 )
                },
                {"role": "user", "content": message}
            ],
            max_tokens=250,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return "Sorry, I couldn't process your request at the moment."

# ---------------------------
# Main response function
# ---------------------------
def enhanced_dental_response(message):
    # First, try keyword-based responses
    reply = dental_ai_response(message)

    # If fallback response detected, use GPT for dental-only intelligent answer
    fallback_keywords = [
        "I can answer questions about dental procedures",
        "Could you tell me more about your dental concern",
        "I'm here to help with dental questions"
    ]
    if any(fk in reply for fk in fallback_keywords):
        return chatgpt_dental_response(message)
    
    return reply

# ---------------------------
# Flask route
# ---------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    reply = enhanced_dental_response(user_input)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
