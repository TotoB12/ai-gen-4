import os
from bardapi import Bard
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
token = os.environ['token']
bard = Bard(token=token)
with open("system_card.txt", "r") as file:
    system = file.read()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_message = data["message"]
    history = data["history"]

    messages = str(system) + str(history) + str(user_message)
    ai_message = bard.get_answer(messages)['content']

    return jsonify(ai_message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
