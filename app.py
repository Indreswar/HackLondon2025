import sys
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import ollama  # Import Ollama for fallback

# ✅ Initialize Flask app
app = Flask(__name__, template_folder="templates")
CORS(app)

# ✅ Fix Import Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# ✅ Import AI Response Function
try:
    from langlogic import generate_response
    print("✅ Successfully imported `generate_response` from langlogic.py")
    use_advanced_ai = True  # Flag to use the main AI function
except ImportError as e:
    print(f"❌ ERROR: Could not import `generate_response` - {e}")
    use_advanced_ai = False  # Switch to basic Ollama AI

@app.route("/", methods=["GET"])
def home():
    """Serves the frontend page."""
    return render_template("index.html")  # Make sure 'templates/index.html' exists

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot requests."""
    user_id = request.json.get("user_id", "default_user")
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "⚠️ Please enter a message!"})

    try:
        # ✅ Use the main AI if available
        if use_advanced_ai:
            response_text = generate_response(user_id, user_message)
        else:
            raise Exception("Switching to basic Ollama")  # Force fallback if AI not available
    except Exception as e:
        print(f"⚠️ AI Processing Error: {e}")
        response_text = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[{"role": "user", "content": user_message}]
        )["message"]["content"]
        

        
        return jsonify({"response": response_text})

import re

def format_text_bold(text):
    """
    Auto-formats key terms by making them bold (`**`).
    Example: "AI is powerful" → "**AI** is **powerful**"
    """
    # Define words to emphasize (add more if needed)
    keywords = ["AI", "intelligence", "learning", "knowledge", "thinking", "reasoning", "memory"]
    
    # Use regex to wrap words in **bold**
    for word in keywords:
        text = re.sub(rf'\b({word})\b', r'**\1**', text, flags=re.IGNORECASE)

    return text




if __name__ == "__main__":
    print("✅ Starting Flask server...")
    app.run(debug=True)
