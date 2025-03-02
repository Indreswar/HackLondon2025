import sys
import os

# Force Python to recognize the 'proxet' directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Debugging: Print current directory and Python's import path
print("✅ Current working directory:", BASE_DIR)  
print("✅ sys.path:", sys.path)  

# Ensure lang_logic.py exists
if not os.path.isfile(os.path.join(BASE_DIR, "lang_logic.py")):
    print("❌ ERROR: lang_logic.py does NOT exist in this directory!")
    exit(1)
else:
    print("✅ lang_logic.py exists!")

# Try importing lang_logic
try:
    from lang_logic import generate_response
    print("✅ Successfully imported lang_logic!")
except ModuleNotFoundError as e:
    print("❌ ERROR: Python still cannot find lang_logic!")
    print(e)
    exit(1)  # Stop execution if lang_logic can't be found

# Flask imports
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot requests."""
    user_id = request.json.get("user_id", "default_user")
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message!"})

    # Get AI response from LangChain + Ollama
    response_text = generate_response(user_id, user_message)

    return jsonify({"response": response_text})

@app.route("/")
def home():
    """Serve the main chat UI."""
    return render_template("index.html")

@app.route("/developer")
def developer_html():
    """Serve the developer UI."""
    return render_template("developer.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
