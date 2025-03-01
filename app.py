from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  

# Serve index.html when user visits "/"
@app.route("/")
def home():
    return render_template("index.html")  # Flask automatically finds it in /templates

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message!"})

    # Send message to DeepSeek 7B
    response = ollama.chat("deepseek-r1:1.5b", messages=[{"role": "user", "content": user_message}])

    return jsonify({"response": response['message']['content']})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
