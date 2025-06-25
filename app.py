from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_message}
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            bot_reply = result['candidates'][0]['content']['parts'][0]['text']
        else:
            bot_reply = f"❌ Error: {response.status_code} - {response.text}"
    except Exception as e:
        bot_reply = f"❌ Exception occurred: {str(e)}"

    return jsonify({"reply": bot_reply})
    
    
if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True)
