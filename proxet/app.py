import sys
import os

# Force Python to recognize local files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Debugging: Print current directory and Python's import path
print("✅ Current working directory:", os.getcwd())  # Debugging
print("✅ sys.path:", sys.path)  # Debugging

# Check if lang_logic.py exists
if not os.path.isfile("lang_logic.py"):
    print("❌ ERROR: lang_logic.py does NOT exist in this directory!")

# Try importing lang_logic
try:
    import lang_logic
    print("✅ Successfully imported lang_logic!")
except ModuleNotFoundError:
    print("❌ ERROR: Python still cannot find lang_logic!")

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from lang_logic import generate_response  # Import AI logic

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_id = request.json.get("user_id", "default_user")
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message!"})

    # Get AI response using LangChain + Ollama
    response_text = generate_response(user_id, user_message)

    return jsonify({"response": response_text})

# Serve index.html when user visits "/"
@app.route("/")
def home():
    return render_template("index.html")

# Serve developer.html
@app.route("/developer")
def developer_html():
    return render_template("developer.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
