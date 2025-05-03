from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your website

@app.route('/')
def home():
    return 'Chatbot backend is up!'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    # Dummy reply for now
    reply = f"You asked: {user_message}. I'm here to help with dental questions!"

    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(debug=True)
