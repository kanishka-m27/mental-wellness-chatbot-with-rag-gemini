from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home route for serve the chat UI
@app.route("/")
def index():
    return render_template("index.html")

# Chat route for simple placeholder response
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Temporary response check
    reply = "I'm your mental wellness assistant. For now, I'm still learning. 💙"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
