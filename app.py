import os
from bardapi import Bard
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24)
token = os.environ['token']

def trim_data(data):
    if len(data) > 5000:
        data = data[:5000]
    return data

with open("system_card.txt", "r") as file:
    system = file.read()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    bard = Bard(token=token)
    data = request.get_json()
    print(data)
    conversation = str(data["history"]) + str(data["message"])
    messages = str(system) + trim_data(conversation)
  
    file = data["file"]
    print(file)
    # file = open(file)
    # filename = file.filename
    # file.save('files/' + filename)
  
    ai_message = bard.get_answer(messages)['content']
    return jsonify(ai_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
