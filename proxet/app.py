from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_logic import generate_response  # Import AI logic

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_id = request.json.get("user_id", "default_user")
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message!"})

    # Get AI response using FAISS + Neo4j + Ollama
    response_text = generate_response(user_id, user_message)

    return jsonify({"response": response_text})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/developer")
def developer_html():
    return render_template("developer.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
