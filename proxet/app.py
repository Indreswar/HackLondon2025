import sys
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

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
except ImportError as e:
    print(f"❌ ERROR: Could not import `generate_response` - {e}")
    exit(1)

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

    # ✅ Get AI response
    response_text = generate_response(user_id, user_message)

    return jsonify({"response": response_text})

if __name__ == "__main__":
    print("✅ Starting Flask server...")
    app.run(debug=True)
