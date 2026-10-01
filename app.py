from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Initialize ChatterBot
chatbot = ChatBot(
    'WebBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///db.sqlite3'
)

# Train the chatbot on English corpus data
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400
    
    # Generate bot response
    bot_response = chatbot.get_response(user_message)
    return jsonify({"response": str(bot_response)})

if __name__ == "__main__":
    app.run(debug=True)