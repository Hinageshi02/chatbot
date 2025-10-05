from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# ---------------------------
# Set OpenAI API Key
# ---------------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")  # or directly: "sk-..."

# ---------------------------
# Optional: Dental price reference (for GPT cost calculations)
# ---------------------------
PRICE_LIST = {
    "consultation": 500,
    "cleaning": 800,
    "deep cleaning": 2000,  # average
    "filling": 800,
    "filling_surface": 200,
    "extraction": 800,
    "difficult extraction": 2000,  # average
    "braces_upper_lower": 30000,
    "braces_complete": 50000,
    "whitening": 6500,  # average
    # You can expand with crowns, dentures, retainers, implants, etc.
}

# ---------------------------
# GPT dental assistant response
# ---------------------------
def chatgpt_dental_response(message):
    """
    Sends user message to GPT-4, instructing it to:
    - Answer any dental-related question worldwide.
    - Provide natural, detailed answers.
    - Estimate total cost if multiple treatments are mentioned (using PRICE_LIST).
    - Refuse politely if question is unrelated to dentistry.
    """
    try:
        system_prompt = (
            "You are a highly knowledgeable professional dental assistant and educator. "
            "Answer ALL dental-related questions accurately, including: "
            "treatments, procedures, oral health advice, global best practices, prices, and appointments. "
            "If the user mentions multiple treatments, calculate an estimated total cost using this reference:\n" +
            "\n".join([f"- {k.replace('_',' ').title()}: ₱{v}" for k,v in PRICE_LIST.items()]) +
            "\nIf the question is unrelated to dentistry, respond politely: "
            "'I'm sorry, I can only answer dental-related questions.' "
            "Be clear, concise, and helpful."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo" if you prefer
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print("GPT Error:", e)
        return "Sorry, I couldn't process your request at the moment."

# ---------------------------
# Flask route
# ---------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input or user_input.strip() == "":
        return jsonify({"response": "Please provide a message."})

    reply = chatgpt_dental_response(user_input)
    return jsonify({"response": reply})

# ---------------------------
# Run the Flask app
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
