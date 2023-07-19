import os
from bardapi import Bard
from flask import Flask, jsonify, render_template, request, session
import re

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
    # try:
    bard = Bard(token=token)
    data = request.get_json()    
    conversation = str(data["history"]) + str(data["message"])
    messages = str(system) + trim_data(conversation)

    ai_gen = bard.get_answer(messages)
    #print(ai_gen)

    ai_message = ai_gen['content']
    print(ai_message)
    
    #   if ai_gen["images"]:
        
    #       print(ai_gen["images"])
    #       image_links = list(ai_gen['images'])
    #       bracket_contents = re.findall(r'\[(.*?)\]', ai_message)
        
    #       for bracket in bracket_contents:
    #           number_images = 1
    #           if bracket.startswith(("1 ", "a ", "an ")):
    #               placeholder_replacement = f"[{image_links.pop(0)}]"
    #           else:
    #               number = re.search(r'^(\d+)', bracket)
    #               if number:
    #                   number_images = int(number.group())
                    
    #               placeholder_replacement = " ".join([f"[{image_links.pop(0)}]" for image_links in range(number_images)])
    #           ai_message = ai_message.replace(f"[{bracket}]", placeholder_replacement, 1)
  
    #   return jsonify(ai_message)
    # except Exception as e:
    #   return e


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
